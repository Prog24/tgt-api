CREATE TABLE user(
  id VARCHAR(36) NOT NULL,
  email VARCHAR(100) UNIQUE,
  password VARCHAR(100),
  ctime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  utime TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO user (id, email, password) VALUES ('87594f99-153d-4f23-8edb-7dc8a3d6cb64', 'example@example.com', '$2b$12$eFVTa1PCT.c9Qjlco.MqCOZSmhULZPRCzuNeWtVGCurCr4NpeOM4G');