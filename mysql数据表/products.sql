-- MySQL 建表语句 for table `products`
-- Generated at: 2026-04-27

CREATE TABLE `products` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `images` json NOT NULL,
  `campus_location` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `building_location` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `seller_id` bigint NOT NULL,
  `stock` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `products_seller_id_76e92f9e_fk_users_id` (`seller_id`),
  CONSTRAINT `products_seller_id_76e92f9e_fk_users_id` FOREIGN KEY (`seller_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
