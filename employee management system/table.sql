CREATE SCHEMA employee_db;

USE employee_db;

ALTER TABLE employees ADD COLUMN department VARCHAR(100);


ALTER TABLE employees ADD COLUMN age INT;





USE employee_db; -- Replace with your actual database name
SET SESSION lock_wait_timeout = 120;
ALTER TABLE employee ADD COLUMN department VARCHAR(100);

ALTER TABLE employee ADD COLUMN email VARCHAR(255);




CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(100),
    status VARCHAR(50),
    date_added DATE
);

SHOW TABLES;



INSERT INTO employees (name, role, status, date_added)
VALUES 
('Alice Johnson', 'Developer', 'Active', '2026-07-15'),
('Bob Smith', 'Designer', 'Active', '2026-07-16');


SELECT * FROM employees;