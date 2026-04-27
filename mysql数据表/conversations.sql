-- MySQL 建表语句 for table `conversations`
-- Generated at: 2026-04-27

CREATE TABLE `conversations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `product_id` bigint NOT NULL,
  `last_message_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `conversations_product_id_c2c693e3_fk_products_id` (`product_id`),
  KEY `conversations_last_message_id_77a159de_fk_messages_id` (`last_message_id`),
  CONSTRAINT `conversations_last_message_id_77a159de_fk_messages_id` FOREIGN KEY (`last_message_id`) REFERENCES `messages` (`id`),
  CONSTRAINT `conversations_product_id_c2c693e3_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
