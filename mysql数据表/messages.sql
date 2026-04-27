-- MySQL 建表语句 for table `messages`
-- Generated at: 2026-04-27

CREATE TABLE `messages` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `conversation_id` bigint NOT NULL,
  `sender_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `messages_conversation_id_5ef638db_fk_conversations_id` (`conversation_id`),
  KEY `messages_sender_id_dc5a0bbd_fk_users_id` (`sender_id`),
  CONSTRAINT `messages_conversation_id_5ef638db_fk_conversations_id` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`),
  CONSTRAINT `messages_sender_id_dc5a0bbd_fk_users_id` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
