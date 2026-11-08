CREATE DATABASE IF NOT EXISTS saintek_overflow
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE saintek_overflow;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'student',
    account_status VARCHAR(30) NOT NULL DEFAULT 'active'
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    tags VARCHAR(255) NULL,
    status ENUM('Open', 'Answered', 'Resolved') NOT NULL DEFAULT 'Open',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_questions_user
        FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_questions_category
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
) ENGINE=InnoDB;

INSERT IGNORE INTO users (user_id, username, email, password, role, account_status)
VALUES (1, 'Mahasiswa Demo', 'demo@saintek-overflow.local', 'demo-only', 'student', 'active');

INSERT IGNORE INTO categories (category_name) VALUES
('Pemrograman'),
('Matematika'),
('Jaringan Komputer'),
('Basis Data'),
('Sistem Informasi'),
('Lainnya');
