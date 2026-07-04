/*
Navicat MySQL Data Transfer

Source Server         : root
Source Server Version : 80046
Source Host           : localhost:3306
Source Database       : campus_trade

Target Server Type    : MYSQL
Target Server Version : 80046
File Encoding         : 65001

Date: 2026-06-09 19:59:42
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `products`
-- ----------------------------
DROP TABLE IF EXISTS `products`;
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of products
-- ----------------------------
INSERT INTO `products` VALUES ('14', '电脑', '九九新，正品', '4500.00', '[\"%E7%94%B5%E8%84%91.jpg\"]', '什邡校区', '1', 'available', '0', '2026-05-29 14:18:04.686995', '2026-06-03 10:11:51.485686', '数码产品', '14', '1');
INSERT INTO `products` VALUES ('15', '鼠标', '二手的', '29.99', '[\"鼠标.png\"]', '成都校区', '2', 'available', '0', '2026-05-29 14:19:31.002695', '2026-06-03 10:44:16.861100', '数码产品', '14', '1');
INSERT INTO `products` VALUES ('16', '插线板', '九九新', '9.99', '[\"插线板.jpg\"]', '成都校区', '12', 'sold', '0', '2026-05-29 14:20:35.582437', '2026-05-29 16:01:08.667820', '生活日用', '14', '1');
