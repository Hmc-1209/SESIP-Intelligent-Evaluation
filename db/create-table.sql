-- Prevent recreating database
DROP DATABASE IF EXISTS `sesip-app`;

CREATE DATABASE `sesip-app`;
USE `sesip-app`;

-- Create USER table
CREATE TABLE User
(
    user_id  INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL
);

-- Create SecurityTarget table
CREATE TABLE SecurityTarget
(
    st_id       INT AUTO_INCREMENT PRIMARY KEY,
    st_name     VARCHAR(50) NOT NULL UNIQUE,
    create_date DATE        NOT NULL,
    update_date DATE        NOT NULL,
    sesip_level INT         NOT NULL,
    is_valid    BOOL        NOT NULL,
    owner_id    INT         NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES User (user_id)
);