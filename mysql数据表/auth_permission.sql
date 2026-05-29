-- Table structure for `auth_permission`
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for `auth_permission`
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('1', 'Can add permission', '1', 'add_permission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('2', 'Can change permission', '1', 'change_permission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('3', 'Can delete permission', '1', 'delete_permission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('4', 'Can view permission', '1', 'view_permission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('5', 'Can add group', '2', 'add_group');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('6', 'Can change group', '2', 'change_group');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('7', 'Can delete group', '2', 'delete_group');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('8', 'Can view group', '2', 'view_group');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('9', 'Can add content type', '3', 'add_contenttype');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('10', 'Can change content type', '3', 'change_contenttype');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('11', 'Can delete content type', '3', 'delete_contenttype');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('12', 'Can view content type', '3', 'view_contenttype');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('13', 'Can add log entry', '4', 'add_logentry');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('14', 'Can change log entry', '4', 'change_logentry');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('15', 'Can delete log entry', '4', 'delete_logentry');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('16', 'Can view log entry', '4', 'view_logentry');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('17', 'Can add session', '5', 'add_session');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('18', 'Can change session', '5', 'change_session');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('19', 'Can delete session', '5', 'delete_session');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('20', 'Can view session', '5', 'view_session');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('21', 'Can add 鐢ㄦ埛', '6', 'add_user');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('22', 'Can change 鐢ㄦ埛', '6', 'change_user');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('23', 'Can delete 鐢ㄦ埛', '6', 'delete_user');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('24', 'Can view 鐢ㄦ埛', '6', 'view_user');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('25', 'Can add 鍒嗙被', '7', 'add_category');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('26', 'Can change 鍒嗙被', '7', 'change_category');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('27', 'Can delete 鍒嗙被', '7', 'delete_category');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('28', 'Can view 鍒嗙被', '7', 'view_category');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('29', 'Can add 鍟嗗搧', '8', 'add_product');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('30', 'Can change 鍟嗗搧', '8', 'change_product');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('31', 'Can delete 鍟嗗搧', '8', 'delete_product');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('32', 'Can view 鍟嗗搧', '8', 'view_product');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('33', 'Can add 浜ゆ槗', '9', 'add_transaction');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('34', 'Can change 浜ゆ槗', '9', 'change_transaction');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('35', 'Can delete 浜ゆ槗', '9', 'delete_transaction');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('36', 'Can view 浜ゆ槗', '9', 'view_transaction');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('37', 'Can add 鎷夐粦', '10', 'add_block');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('38', 'Can change 鎷夐粦', '10', 'change_block');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('39', 'Can delete 鎷夐粦', '10', 'delete_block');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('40', 'Can view 鎷夐粦', '10', 'view_block');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('41', 'Can add 浼氳瘽', '11', 'add_conversation');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('42', 'Can change 浼氳瘽', '11', 'change_conversation');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('43', 'Can delete 浼氳瘽', '11', 'delete_conversation');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('44', 'Can view 浼氳瘽', '11', 'view_conversation');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('45', 'Can add 鏀惰棌', '12', 'add_favorite');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('46', 'Can change 鏀惰棌', '12', 'change_favorite');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('47', 'Can delete 鏀惰棌', '12', 'delete_favorite');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('48', 'Can view 鏀惰棌', '12', 'view_favorite');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('49', 'Can add 娑堟伅', '13', 'add_message');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('50', 'Can change 娑堟伅', '13', 'change_message');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('51', 'Can delete 娑堟伅', '13', 'delete_message');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('52', 'Can view 娑堟伅', '13', 'view_message');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('53', 'Can add 涓炬姤', '14', 'add_report');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('54', 'Can change 涓炬姤', '14', 'change_report');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('55', 'Can delete 涓炬姤', '14', 'delete_report');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('56', 'Can view 涓炬姤', '14', 'view_report');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('57', 'Can add 璇勮', '15', 'add_comment');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('58', 'Can change 璇勮', '15', 'change_comment');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('59', 'Can delete 璇勮', '15', 'delete_comment');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('60', 'Can view 璇勮', '15', 'view_comment');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('61', 'Can add permission', '2', 'add_permission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('62', 'Can change permission', '2', 'change_permission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('63', 'Can delete permission', '2', 'delete_permission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('64', 'Can view permission', '2', 'view_permission');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('65', 'Can add group', '1', 'add_group');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('66', 'Can change group', '1', 'change_group');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('67', 'Can delete group', '1', 'delete_group');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('68', 'Can view group', '1', 'view_group');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('69', 'Can add 用户', '4', 'add_user');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('70', 'Can change 用户', '4', 'change_user');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('71', 'Can delete 用户', '4', 'delete_user');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('72', 'Can view 用户', '4', 'view_user');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('73', 'Can add 分类', '5', 'add_category');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('74', 'Can change 分类', '5', 'change_category');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('75', 'Can delete 分类', '5', 'delete_category');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('76', 'Can view 分类', '5', 'view_category');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('77', 'Can add 商品', '6', 'add_product');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('78', 'Can change 商品', '6', 'change_product');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('79', 'Can delete 商品', '6', 'delete_product');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('80', 'Can view 商品', '6', 'view_product');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('81', 'Can add 交易', '7', 'add_transaction');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('82', 'Can change 交易', '7', 'change_transaction');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('83', 'Can delete 交易', '7', 'delete_transaction');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('84', 'Can view 交易', '7', 'view_transaction');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('85', 'Can add log entry', '8', 'add_logentry');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('86', 'Can change log entry', '8', 'change_logentry');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('87', 'Can delete log entry', '8', 'delete_logentry');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('88', 'Can view log entry', '8', 'view_logentry');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('89', 'Can add session', '9', 'add_session');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('90', 'Can change session', '9', 'change_session');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('91', 'Can delete session', '9', 'delete_session');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('92', 'Can view session', '9', 'view_session');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('93', 'Can add 评论', '10', 'add_comment');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('94', 'Can change 评论', '10', 'change_comment');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('95', 'Can delete 评论', '10', 'delete_comment');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('96', 'Can view 评论', '10', 'view_comment');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('97', 'Can add 消息', '12', 'add_message');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('98', 'Can change 消息', '12', 'change_message');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('99', 'Can delete 消息', '12', 'delete_message');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('100', 'Can view 消息', '12', 'view_message');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('101', 'Can add 收藏', '13', 'add_favorite');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('102', 'Can change 收藏', '13', 'change_favorite');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('103', 'Can delete 收藏', '13', 'delete_favorite');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('104', 'Can view 收藏', '13', 'view_favorite');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('105', 'Can add 拉黑', '15', 'add_block');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('106', 'Can change 拉黑', '15', 'change_block');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('107', 'Can delete 拉黑', '15', 'delete_block');
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES ('108', 'Can view 拉黑', '15', 'view_block');

