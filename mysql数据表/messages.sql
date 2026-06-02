-- Table: messages
CREATE TABLE `messages` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `conversation_id` bigint NOT NULL,
  `sender_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `messages_conversation_id_5ef638db_fk_conversations_id` (`conversation_id`),
  KEY `messages_sender_id_dc5a0bbd_fk_users_id` (`sender_id`),
  CONSTRAINT `messages_conversation_id_5ef638db_fk_conversations_id` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`),
  CONSTRAINT `messages_sender_id_dc5a0bbd_fk_users_id` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (1, '您好，我想咨询关于\"红苹果\"的商品', 1, 2026-05-19 18:25:39.630014, 1, 12);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (2, '贵点卖不', 1, 2026-05-19 18:25:51.495398, 1, 12);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (3, '您好，我想咨询关于\"青苹果\"的商品', 1, 2026-05-19 18:40:02.388716, 2, 12);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (4, '你好，苹果包好吃的吗？', 1, 2026-05-19 18:40:24.526873, 2, 12);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (5, '那肯定的！', 1, 2026-05-19 18:40:42.848514, 2, 6);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (6, '您好，我想咨询关于\"山竹\"的商品', 1, 2026-05-19 19:00:38.905103, 3, 12);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (7, '贵点卖不？', 1, 2026-05-19 19:00:46.420037, 3, 12);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (8, '好啊。', 1, 2026-05-19 19:00:59.144145, 3, 6);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (9, '您好，我想咨询关于\"电脑\"的商品', 1, 2026-05-29 14:34:53.483112, 4, 15);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (10, '您好，我想咨询关于\"电脑\"的商品', 1, 2026-05-29 14:35:01.707219, 4, 15);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (11, '你好', 1, 2026-05-29 14:38:48.959261, 4, 15);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (12, '可以便宜吗？', 1, 2026-05-29 14:39:01.994671, 4, 15);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (13, '不可以', 1, 2026-05-29 14:39:20.784739, 4, 14);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (14, '。', 1, 2026-05-29 14:54:59.614719, 4, 14);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (15, '。', 1, 2026-05-29 14:55:17.337274, 4, 15);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (16, '您好，我想咨询关于\"鼠标\"的商品', 0, 2026-05-29 14:55:27.014581, 5, 15);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (17, '。', 0, 2026-05-29 14:55:30.879990, 5, 15);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (18, '您好，我想咨询关于\"电脑\"的商品', 0, 2026-06-02 08:08:46.630972, 6, 17);
INSERT INTO messages (id, content, is_read, created_at, conversation_id, sender_id) VALUES (19, '你好你好', 0, 2026-06-02 08:08:55.841197, 6, 17);
