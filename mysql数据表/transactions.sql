-- 表: transactions
CREATE TABLE `transactions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `locked_until` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `buyer_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  `seller_id` bigint NOT NULL,
  `recipient_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `recipient_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `shipping_address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `transactions_buyer_id_72af2b81_fk_users_id` (`buyer_id`),
  KEY `transactions_product_id_b82fbdba_fk_products_id` (`product_id`),
  KEY `transactions_seller_id_72f36279_fk_users_id` (`seller_id`),
  CONSTRAINT `transactions_buyer_id_72af2b81_fk_users_id` FOREIGN KEY (`buyer_id`) REFERENCES `users` (`id`),
  CONSTRAINT `transactions_product_id_b82fbdba_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `transactions_seller_id_72f36279_fk_users_id` FOREIGN KEY (`seller_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
