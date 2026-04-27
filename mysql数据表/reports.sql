-- MySQL 建表语句 for table `reports`
-- Generated at: 2026-04-27

CREATE TABLE `reports` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `reason` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `product_id` bigint NOT NULL,
  `reported_user_id` bigint NOT NULL,
  `reporter_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reports_product_id_228583b1_fk_products_id` (`product_id`),
  KEY `reports_reported_user_id_ca2aab2b_fk_users_id` (`reported_user_id`),
  KEY `reports_reporter_id_ef570044_fk_users_id` (`reporter_id`),
  CONSTRAINT `reports_product_id_228583b1_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `reports_reported_user_id_ca2aab2b_fk_users_id` FOREIGN KEY (`reported_user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `reports_reporter_id_ef570044_fk_users_id` FOREIGN KEY (`reporter_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
