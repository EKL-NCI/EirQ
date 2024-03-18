CREATE DATABASE IF NOT EXISTS EirQ;
USE EirQ;

-- Create a table named users
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO users (username, email, password) VALUES ('john_doe', 'john@example.com', 'hashed_password_123');
INSERT INTO users (username, email, password) VALUES ('jane_smith', 'jane@example.com', 'hashed_password_456');
INSERT INTO users (username, email, password) VALUES ('alex_brown', 'alex@example.com', 'hashed_password_789');