-- Table structure for `django_content_type`
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for `django_content_type`
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('8', 'admin', 'logentry');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('1', 'auth', 'group');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('2', 'auth', 'permission');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('15', 'communications', 'block');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('10', 'communications', 'comment');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('11', 'communications', 'conversation');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('13', 'communications', 'favorite');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('12', 'communications', 'message');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('14', 'communications', 'report');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('3', 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('5', 'products', 'category');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('6', 'products', 'product');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('9', 'sessions', 'session');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('7', 'transactions', 'transaction');
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES ('4', 'users', 'user');

