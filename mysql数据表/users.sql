-- Table structure for `users`
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `student_id` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `grade` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `major` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatar` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `student_id` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for `users`
INSERT INTO `users` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `name`, `student_id`, `grade`, `major`, `avatar`, `gender`) VALUES ('14', 'pbkdf2_sha256$600000$20bGKpacK3Ol7lPr6FE2Vc$KdEHoIgbwUO1zkq4AM4nv8IrqA7sBOYQMgmoy36gLIs=', NULL, '0', '12345678', '', '', '', '0', '1', '2026-05-29 14:07:07.486549', '小王', '12345678', '2023级', '软件工程', '', NULL);
INSERT INTO `users` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `name`, `student_id`, `grade`, `major`, `avatar`, `gender`) VALUES ('15', 'pbkdf2_sha256$600000$6jZx4Lxkn6C8a7hr7unwTc$pjaV6UOHFwjHb4OboA07CEY17ELjjbQlDlMwa7RTziw=', NULL, '0', '12345677', '', '', '', '0', '1', '2026-05-29 14:27:45.811744', '小何', '12345677', '2022级', '计算机科学与技术', '', NULL);
INSERT INTO `users` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `name`, `student_id`, `grade`, `major`, `avatar`, `gender`) VALUES ('16', 'pbkdf2_sha256$600000$U6IurYrqDgojl0oqze8peV$AlsDGBUtVPKbYYadvAZ02zCwFcoStrMXUT/0P8ctP9c=', NULL, '1', '00000000', '', '', '', '0', '1', '2026-05-29 16:17:19.547387', 'admin', '00000000', NULL, NULL, '', NULL);

