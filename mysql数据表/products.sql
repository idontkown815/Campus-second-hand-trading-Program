-- Table: products
CREATE TABLE `products` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `images` json NOT NULL,
  `campus_location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `building_location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `seller_id` bigint NOT NULL,
  `stock` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `products_seller_id_76e92f9e_fk_users_id` (`seller_id`),
  CONSTRAINT `products_seller_id_76e92f9e_fk_users_id` FOREIGN KEY (`seller_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO products (id, title, description, price, images, campus_location, building_location, status, is_deleted, created_at, updated_at, category, seller_id, stock) VALUES (14, '电脑', '九九新，正品', 4500.00, '[\"%E7%94%B5%E8%84%91.jpg\"]', '什邡校区', '1', 'available', 0, 2026-05-29 14:18:04.686995, 2026-06-02 08:09:21.179826, '数码产品', 14, 1);
INSERT INTO products (id, title, description, price, images, campus_location, building_location, status, is_deleted, created_at, updated_at, category, seller_id, stock) VALUES (15, '鼠标', '二手的', 29.99, '[\"鼠标.png\"]', '成都校区', '2', 'available', 0, 2026-05-29 14:19:31.002695, 2026-05-29 14:19:31.002695, '数码产品', 14, 1);
INSERT INTO products (id, title, description, price, images, campus_location, building_location, status, is_deleted, created_at, updated_at, category, seller_id, stock) VALUES (16, '插线板', '九九新', 9.99, '[\"插线板.jpg\"]', '成都校区', '12', 'sold', 0, 2026-05-29 14:20:35.582437, 2026-05-29 16:01:08.667820, '生活日用', 14, 1);
