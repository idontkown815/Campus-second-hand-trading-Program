-- MySQL 建表语句 for table `blocks`
-- Generated at: 2026-04-27

CREATE TABLE `blocks` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `blocked_id` bigint NOT NULL,
  `blocker_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `blocks_blocker_id_blocked_id_f4cabc84_uniq` (`blocker_id`,`blocked_id`),
  KEY `blocks_blocked_id_bd10efad_fk_users_id` (`blocked_id`),
  CONSTRAINT `blocks_blocked_id_bd10efad_fk_users_id` FOREIGN KEY (`blocked_id`) REFERENCES `users` (`id`),
  CONSTRAINT `blocks_blocker_id_c428556e_fk_users_id` FOREIGN KEY (`blocker_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
