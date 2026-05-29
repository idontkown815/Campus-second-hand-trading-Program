-- Table structure for `conversations_participants`
DROP TABLE IF EXISTS `conversations_participants`;
CREATE TABLE `conversations_participants` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `conversation_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `conversations_participants_conversation_id_user_id_7f9cba6f_uniq` (`conversation_id`,`user_id`),
  KEY `conversations_participants_user_id_968b244f_fk_users_id` (`user_id`),
  CONSTRAINT `conversations_partic_conversation_id_988acf55_fk_conversat` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`),
  CONSTRAINT `conversations_participants_user_id_968b244f_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for `conversations_participants`
INSERT INTO `conversations_participants` (`id`, `conversation_id`, `user_id`) VALUES ('2', '1', '6');
INSERT INTO `conversations_participants` (`id`, `conversation_id`, `user_id`) VALUES ('1', '1', '12');
INSERT INTO `conversations_participants` (`id`, `conversation_id`, `user_id`) VALUES ('4', '2', '6');
INSERT INTO `conversations_participants` (`id`, `conversation_id`, `user_id`) VALUES ('3', '2', '12');
INSERT INTO `conversations_participants` (`id`, `conversation_id`, `user_id`) VALUES ('6', '3', '6');
INSERT INTO `conversations_participants` (`id`, `conversation_id`, `user_id`) VALUES ('5', '3', '12');
INSERT INTO `conversations_participants` (`id`, `conversation_id`, `user_id`) VALUES ('7', '4', '14');
INSERT INTO `conversations_participants` (`id`, `conversation_id`, `user_id`) VALUES ('8', '4', '15');
INSERT INTO `conversations_participants` (`id`, `conversation_id`, `user_id`) VALUES ('9', '5', '14');
INSERT INTO `conversations_participants` (`id`, `conversation_id`, `user_id`) VALUES ('10', '5', '15');

