DROP DATABASE IF EXISTS corp_vault_db;
CREATE DATABASE corp_vault_db;
USE corp_vault_db;

-- Division Table
CREATE TABLE Divisions(
    division_code INT PRIMARY KEY,
    division_title VARCHAR(60)
);

-- Personnel Table (Synchronized with Flask app, without compensation, plaintext passwords)
CREATE TABLE personnel(
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(60),
    mobile_number VARCHAR(15),
    email VARCHAR(100),
    username VARCHAR(50),
    password VARCHAR(255),
    role VARCHAR(20) DEFAULT 'employee',
    onboarding_date DATE DEFAULT (CURRENT_DATE),
    division_code INT,
    FOREIGN KEY (division_code) REFERENCES Divisions(division_code)
);

-- Insert Division Data
INSERT INTO Divisions VALUES
(10, 'Human Capital'),
(20, 'Systems Engineering'),
(30, 'Capital Markets'),
(40, 'Brand Strategy');

-- Insert Initial Personnel Records (Including Default Admin & HR Accounts with Plaintext Passwords)
INSERT INTO personnel (id, full_name, mobile_number, email, username, password, role, onboarding_date, division_code) VALUES
(1, 'Director Master', '9876543210', 'admin@nexus.corp', 'director', 'masterkey', 'admin', '2025-01-01', 20),
(2, 'Supervisor Key', '9876543211', 'hr@nexus.corp', 'supervisor', 'keypass', 'hr', '2025-01-01', 10),
(1001, 'Aditya', '9811111110', 'aditya@nexus.corp', 'aditya', 'pass123', 'employee', '2025-02-10', 10),
(1002, 'Rohan', '9822222220', 'rohan@nexus.corp', 'rohan', 'pass123', 'employee', '2025-03-15', 20),
(1003, 'Siddharth', '9833333330', 'siddharth@nexus.corp', 'siddharth', 'pass123', 'employee', '2025-04-20', 20),
(1004, 'Pallavi', '9844444440', 'pallavi@nexus.corp', 'pallavi', 'pass123', 'employee', '2025-05-01', 30),
(1005, 'Varun', '9855555550', 'varun@nexus.corp', 'varun', 'pass123', 'employee', '2025-01-18', 20),
(1006, 'Nidhi', '9866666660', 'nidhi@nexus.corp', 'nidhi', 'pass123', 'employee', '2025-06-01', 40),
(1007, 'Raghav', '9877777770', 'raghav@nexus.corp', 'raghav', 'pass123', 'employee', '2025-02-28', 30),
(1008, 'Ananya', '9888888880', 'ananya@nexus.corp', 'ananya', 'pass123', 'employee', '2025-05-15', 10),
(1009, 'Kunal', '9899999990', 'kunal@nexus.corp', 'kunal', 'pass123', 'employee', '2025-04-10', 40),
(1010, 'Preeti', '9800000000', 'preeti@nexus.corp', 'preeti', 'pass123', 'employee', '2025-03-05', 20);

-- Analytics Queries (Corrected column names and syntax)
-- 1. Division Wise Personnel Count
SELECT dv.division_title,
COUNT(p.id) AS total_headcount
FROM Divisions dv
JOIN personnel p
ON dv.division_code = p.division_code
GROUP BY dv.division_title;

-- 2. Inner Join
SELECT p.id,
p.full_name,
dv.division_title
FROM personnel p
INNER JOIN Divisions dv
ON p.division_code = dv.division_code;

-- 3. Left Join
SELECT p.id,
p.full_name,
dv.division_title
FROM personnel p
LEFT JOIN Divisions dv
ON p.division_code = dv.division_code;

-- 4. Group By With Having
SELECT division_code,
COUNT(*) AS headcount_per_div
FROM personnel
GROUP BY division_code
HAVING COUNT(*) > 2;

-- 5. Personnel Onboarded In Last 6 Months
SELECT *
FROM personnel
WHERE onboarding_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH);

-- 6. Find Duplicate Records
SELECT full_name,
COUNT(*) AS occurrence_count
FROM personnel
GROUP BY full_name
HAVING COUNT(*) > 1;

-- 7. Remove Duplicate Records (Safe Mode Handled)
SET SQL_SAFE_UPDATES = 0;

DELETE p1 
FROM personnel p1 
INNER JOIN personnel p2 
ON p1.full_name = p2.full_name 
AND p1.id > p2.id;

SET SQL_SAFE_UPDATES = 1;
























UPDATE employees SET name = 'Your Name', mobile = '1234567890' WHERE id = 1011;


USE corp_vault_db;
SELECT username, password, role FROM personnel WHERE role = 'admin';

























USE corp_vault_db;
SHOW TABLES;
DESCRIBE Personnel;
SHOW COLUMNS FROM Divisions;

USE corp_vault_db;
SELECT * FROM Personnel;