-- MySQL 建表语句 for table `conversations_participants`
-- Generated at: 2026-04-27

CREATE TABLE `conversations_participants` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `conversation_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `conversations_participants_conversation_id_user_id_7f9cba6f_uniq` (`conversation_id`,`user_id`),
  KEY `conversations_participants_user_id_968b244f_fk_users_id` (`user_id`),
  CONSTRAINT `conversations_partic_conversation_id_988acf55_fk_conversat` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`),
  CONSTRAINT `conversations_participants_user_id_968b244f_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
