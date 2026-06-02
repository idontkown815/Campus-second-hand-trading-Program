-- Table: comments
CREATE TABLE `comments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `comments_product_id` (`product_id`),
  KEY `comments_user_id` (`user_id`),
  CONSTRAINT `comments_product_id_fk` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
  CONSTRAINT `comments_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO comments (id, product_id, user_id, content, created_at) VALUES (1, 8, 12, '真的好吃吗？', 2026-05-19 18:41:13.547968);
INSERT INTO comments (id, product_id, user_id, content, created_at) VALUES (2, 8, 12, '你说中国人不骗中国人。', 2026-05-19 18:41:27.043805);
INSERT INTO comments (id, product_id, user_id, content, created_at) VALUES (3, 8, 12, '你说啊。', 2026-05-19 18:41:32.049828);
INSERT INTO comments (id, product_id, user_id, content, created_at) VALUES (7, 14, 14, '欢迎咨询！！', 2026-05-29 14:29:07.804213);
