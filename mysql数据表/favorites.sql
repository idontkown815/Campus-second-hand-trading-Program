-- MySQL 建表语句 for table `favorites`
-- Generated at: 2026-04-27

CREATE TABLE `favorites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `product_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `favorites_user_id_product_id_30a992ff_uniq` (`user_id`,`product_id`),
  KEY `favorites_product_id_20deaadd_fk_products_id` (`product_id`),
  CONSTRAINT `favorites_product_id_20deaadd_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `favorites_user_id_d60eb79f_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
