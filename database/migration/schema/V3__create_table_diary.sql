CREATE TABLE diary(
  id VARCHAR(36) NOT NULL,
  user_id VARCHAR(36),
  main_text TEXT,
  sub_text TEXT,
  lat VARCHAR(36),
  lon VARCHAR(36),
  ctime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  utime TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO diary (id, user_id, main_text, sub_text, lat, lon) VALUES ('9dd5192b-70fc-429a-8aed-a4fe60fe9a1f', '87594f99-153d-4f23-8edb-7dc8a3d6cb64', 'メインテキストだよ', 'サブテキストだよ', '0', '0');