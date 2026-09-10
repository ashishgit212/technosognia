DROP DATABASE IF EXISTS corp_vault_db;
CREATE DATABASE corp_vault_db;
USE corp_vault_db;

-- Division Table
CREATE TABLE Divisions(
    division_code INT PRIMARY KEY,
    division_title VARCHAR(60)
);

-- Personnel Table
CREATE TABLE Personnel(
    personnel_id INT PRIMARY KEY,
    full_name VARCHAR(60),
    compensation DECIMAL(12,2),
    onboarding_date DATE,
    division_code INT,
    FOREIGN KEY (division_code) REFERENCES Divisions(division_code)
);

-- Insert Division Data
INSERT INTO Divisions VALUES
(10, 'Human Capital'),
(20, 'Systems Engineering'),
(30, 'Capital Markets'),
(40, 'Brand Strategy');

-- Insert Personnel Data
INSERT INTO Personnel VALUES
(1001, 'Aditya', 52000, '2025-02-10', 10),
(1002, 'Rohan', 72000, '2025-03-15', 20),
(1003, 'Siddharth', 91000, '2025-04-20', 20),
(1004, 'Pallavi', 67000, '2025-05-01', 30),
(1005, 'Varun', 83000, '2025-01-18', 20),
(1006, 'Nidhi', 58000, '2025-06-01', 40),
(1007, 'Raghav', 98000, '2025-02-28', 30),
(1008, 'Ananya', 61000, '2025-05-15', 10),
(1009, 'Kunal', 77000, '2025-04-10', 40),
(1010, 'Preeti', 88000, '2025-03-05', 20);

-- 1. Top 5 Highest Compensated Personnel
SELECT *
FROM Personnel
ORDER BY compensation DESC
LIMIT 5;

-- 2. Division Wise Personnel Count
SELECT dv.division_title,
COUNT(p.personnel_id) AS total_headcount
FROM Divisions dv
JOIN Personnel p
ON dv.division_code = p.division_code
GROUP BY dv.division_title;

-- 3. Find Second Highest Compensation
SELECT MAX(compensation) AS runner_up_compensation
FROM Personnel
WHERE compensation <
(
SELECT MAX(compensation)
FROM Personnel
);

-- 4. Personnel Earning Above Division Average Compensation
SELECT full_name, compensation, division_code
FROM Personnel pr
WHERE compensation >
(
SELECT AVG(compensation)
FROM Personnel
WHERE division_code = pr.division_code
);

-- 5. Inner Join
SELECT p.personnel_id,
p.full_name,
dv.division_title
FROM Personnel p
INNER JOIN Divisions dv
ON p.division_code = dv.division_code;

-- 6. Left Join
SELECT p.personnel_id,
p.full_name,
dv.division_title
FROM Personnel p
LEFT JOIN Divisions dv
ON p.division_code = dv.division_code;

-- 7. Group By With Having
SELECT division_code,
COUNT(*) AS headcount_per_div
FROM Personnel
GROUP BY division_code
HAVING COUNT(*) > 2;

-- 8. Personnel Onboarded In Last 6 Months
SELECT *
FROM Personnel
WHERE onboarding_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH);

-- 9. Find Duplicate Records
SELECT full_name,
COUNT(*) AS occurrence_count
FROM Personnel
GROUP BY full_name
HAVING COUNT(*) > 1;

-- 10. Remove Duplicate Records (Safe Mode Handled)
SET SQL_SAFE_UPDATES = 0;

DELETE p1 
FROM Personnel p1 
INNER JOIN Personnel p2 
ON p1.full_name = p2.full_name 
AND p1.personnel_id > p2.personnel_id;

SET SQL_SAFE_UPDATES = 1;