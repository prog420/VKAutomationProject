CREATE DATABASE IF NOT EXISTS vk_db;
USE vk_db;
CREATE TABLE test_users (
    id int NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    surname varchar(255) NOT NULL,
    middle_name varchar(255) DEFAULT NULL,
    username varchar(16) DEFAULT NULL,
    password varchar(255) NOT NULL,
    email varchar(64) NOT NULL,
    access smallint DEFAULT NULL,
    active smallint DEFAULT NULL,
    start_active_time datetime DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY email (email),
    UNIQUE KEY ix_test_users_username (username)
);
SELECT * FROM test_users;

CREATE USER 'test_qa'@'%' IDENTIFIED BY 'qa_test';
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT ON vk_db.test_users TO 'test_qa'@'%';
SELECT * FROM mysql.user;