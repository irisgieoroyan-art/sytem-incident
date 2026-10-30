CREATE DATABASE IF NOT EXISTS incident_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE incident_db;

CREATE TABLE IF NOT EXISTS incident_reports (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ir_no VARCHAR(12) NOT NULL UNIQUE,
  reported_by VARCHAR(150) NOT NULL,
  incident_date DATE NOT NULL,
  incident_time TIME NOT NULL,
  location VARCHAR(120) NOT NULL,
  incident_type VARCHAR(60) NOT NULL,
  persons_involved VARCHAR(255) NOT NULL,
  narrative TEXT NOT NULL,
  action_taken TEXT NULL,
  reported_to VARCHAR(120) NULL,
  status VARCHAR(40) NOT NULL DEFAULT 'Kasalukuyang Binabantayan',
  encoded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
