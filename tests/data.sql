INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO url (owner_id, long_url, created)
VALUES
  (1, 'www.huawei.com', '2018-09-11 18:22:27'),
  (1, 'www.baidu.com', '2018-09-11 18:30:50');
  