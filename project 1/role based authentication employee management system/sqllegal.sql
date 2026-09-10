CREATE DATABASE IF NOT EXISTS legal_contract_db;
USE legal_contract_db;

-- Temporarily disable foreign key checks to prevent dependency conflict errors when dropping tables
SET FOREIGN_KEY_CHECKS = 0;

-- Drop existing tables safely
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS modification_requests;
DROP TABLE IF EXISTS contracts;
DROP TABLE IF EXISTS users;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Create users table supporting authentication roles and passwords
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create contracts table with approval statuses and review fields
CREATE TABLE contracts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_by VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    approver_comment TEXT,
    rejection_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create documents table referenced by the foreign key constraint
CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contract_id INT NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    uploaded_by VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE
);

-- Create modification requests table for clause-level changes
CREATE TABLE modification_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contract_id INT NOT NULL,
    contract_title VARCHAR(255) NOT NULL,
    clause_title VARCHAR(255),
    request_type VARCHAR(50) NOT NULL,
    original_value TEXT,
    proposed_modification TEXT NOT NULL,
    reason TEXT NOT NULL,
    requested_by VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    approver_comment TEXT,
    rejection_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE
);

-- Insert initial sample users (Default credentials: admin / admin123 and employee1 / user123)
INSERT INTO users (username, password, role) VALUES 
('admin', 'admin123', 'admin'),
('employee1', 'user123', 'user');

-- View all tables and contents
SHOW TABLES;
SELECT * FROM users;
SELECT * FROM contracts;
SELECT * FROM modification_requests;








USE legal_contract_db;
SELECT id, title, status, created_by FROM contracts;








































USE legal_contract_db;

-- See all tables in the database
SHOW TABLES;

-- View users
SELECT * FROM users;

-- View created contracts
SELECT * FROM contracts;

-- View modification requests submitted by users
SELECT * FROM modification_requests;









USE legal_contract_db;
SELECT id, title, status, created_by FROM contracts;


USE legal_contract_db;

DROP TABLE IF EXISTS audit_logs;

CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    username VARCHAR(50) NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    details TEXT NOT NULL
);


