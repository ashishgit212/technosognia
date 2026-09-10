USE employee_db;
DROP TABLE IF EXISTS employees;



CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(100),
    email VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);












USE employee_db;
ALTER TABLE employees ADD COLUMN role VARCHAR(50) DEFAULT 'Employee';
ALTER TABLE employees ADD COLUMN role VARCHAR(50) DEFAULT 'Employee';
select * from employees;
ALTER TABLE employees ADD COLUMN role VARCHAR(50) DEFAULT 'Employee';
ALTER TABLE employees ADD COLUMN password VARCHAR(255);











USE employee_db;
ALTER TABLE employees ADD COLUMN status VARCHAR(50);
















CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

USE employee_db;
ALTER TABLE employees ADD COLUMN email VARCHAR(150);









CREATE SCHEMA employee_db;

USE employee_db;

ALTER TABLE employees ADD COLUMN department VARCHAR(100);


ALTER TABLE employees ADD COLUMN age INT;





USE employee_db; -- Replace with your actual database name
SET SESSION lock_wait_timeout = 120;
ALTER TABLE employee ADD COLUMN department VARCHAR(100);

ALTER TABLE employee ADD COLUMN email VARCHAR(255);

USE employee_db;
ALTER TABLE employee ADD COLUMN status VARCHAR(20) DEFAULT 'Active';
ALTER TABLE employee ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;


ALTER TABLE employee ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;



DESCRIBE employees; -- Or DESCRIBE employee; depending on your table name














ALTER TABLE employees ADD COLUMN department VARCHAR(100);





DROP TABLE IF EXISTS employee;
ALTER TABLE employees ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

SHOW TABLES;
ALTER TABLE employee ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE employees ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;





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
SELECT * FROM employes;











SET GLOBAL net_read_timeout = 600;
SET GLOBAL net_write_timeout = 600;
SET GLOBAL interactive_timeout = 600;
SET GLOBAL wait_timeout = 600;


