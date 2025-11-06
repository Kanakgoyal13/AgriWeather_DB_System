-- Create Users table and insert sample users for AgriWeather_DB_System

USE Agriculture_Weather_db_system;

CREATE TABLE IF NOT EXISTS Users (
  Username VARCHAR(50) PRIMARY KEY,
  Password VARCHAR(255) NOT NULL,
  Role VARCHAR(20) NOT NULL
);

-- Insert a default admin and a normal user (plaintext password used to match the Streamlit app's check)
INSERT INTO Users (Username, Password, Role)
SELECT 'admin', 'admin123', 'Admin' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM Users WHERE Username = 'admin');

INSERT INTO Users (Username, Password, Role)
SELECT 'user', 'userpass', 'User' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM Users WHERE Username = 'user');
