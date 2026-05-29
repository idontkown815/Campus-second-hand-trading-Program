-- Table structure for `conversations`
DROP TABLE IF EXISTS `conversations`;
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for `conversations`
INSERT INTO `conversations` (`id`, `created_at`, `updated_at`, `product_id`, `last_message_id`) VALUES ('1', '2026-05-19 18:25:39.621743', '2026-05-19 18:25:51.500201', '7', '2');
INSERT INTO `conversations` (`id`, `created_at`, `updated_at`, `product_id`, `last_message_id`) VALUES ('2', '2026-05-19 18:40:02.382046', '2026-05-19 18:40:42.850560', '8', '5');
INSERT INTO `conversations` (`id`, `created_at`, `updated_at`, `product_id`, `last_message_id`) VALUES ('3', '2026-05-19 19:00:38.897272', '2026-05-19 19:00:59.146905', '10', '8');
INSERT INTO `conversations` (`id`, `created_at`, `updated_at`, `product_id`, `last_message_id`) VALUES ('4', '2026-05-29 14:34:53.471923', '2026-05-29 14:55:17.339310', '14', '15');
INSERT INTO `conversations` (`id`, `created_at`, `updated_at`, `product_id`, `last_message_id`) VALUES ('5', '2026-05-29 14:55:27.006011', '2026-05-29 14:55:30.885071', '15', '17');

