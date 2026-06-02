-- Table: django_migrations
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO django_migrations (id, app, name, applied) VALUES (1, 'contenttypes', '0001_initial', 2026-05-19 18:18:57.673290);
INSERT INTO django_migrations (id, app, name, applied) VALUES (2, 'contenttypes', '0002_remove_content_type_name', 2026-05-19 18:19:12.622956);
INSERT INTO django_migrations (id, app, name, applied) VALUES (3, 'auth', '0001_initial', 2026-05-19 18:19:12.626478);
INSERT INTO django_migrations (id, app, name, applied) VALUES (4, 'auth', '0002_alter_permission_name_max_length', 2026-05-19 18:19:12.629011);
INSERT INTO django_migrations (id, app, name, applied) VALUES (5, 'auth', '0003_alter_user_email_max_length', 2026-05-19 18:19:12.631697);
INSERT INTO django_migrations (id, app, name, applied) VALUES (6, 'auth', '0004_alter_user_username_opts', 2026-05-19 18:19:12.634844);
INSERT INTO django_migrations (id, app, name, applied) VALUES (7, 'auth', '0005_alter_user_last_login_null', 2026-05-19 18:19:12.638193);
INSERT INTO django_migrations (id, app, name, applied) VALUES (8, 'auth', '0006_require_contenttypes_0002', 2026-05-19 18:19:12.639298);
INSERT INTO django_migrations (id, app, name, applied) VALUES (9, 'auth', '0007_alter_validators_add_error_messages', 2026-05-19 18:19:12.641835);
INSERT INTO django_migrations (id, app, name, applied) VALUES (10, 'auth', '0008_alter_user_username_max_length', 2026-05-19 18:19:12.644093);
INSERT INTO django_migrations (id, app, name, applied) VALUES (11, 'auth', '0009_alter_user_last_name_max_length', 2026-05-19 18:19:12.645610);
INSERT INTO django_migrations (id, app, name, applied) VALUES (12, 'auth', '0010_alter_group_name_max_length', 2026-05-19 18:19:12.646647);
INSERT INTO django_migrations (id, app, name, applied) VALUES (13, 'auth', '0011_update_proxy_permissions', 2026-05-19 18:19:12.649174);
INSERT INTO django_migrations (id, app, name, applied) VALUES (14, 'auth', '0012_alter_user_first_name_max_length', 2026-05-19 18:19:12.651718);
INSERT INTO django_migrations (id, app, name, applied) VALUES (15, 'users', '0001_initial', 2026-05-19 18:19:12.654261);
INSERT INTO django_migrations (id, app, name, applied) VALUES (16, 'products', '0001_initial', 2026-05-19 18:19:12.655775);
INSERT INTO django_migrations (id, app, name, applied) VALUES (17, 'products', '0002_initial', 2026-05-19 18:19:12.656818);
INSERT INTO django_migrations (id, app, name, applied) VALUES (18, 'transactions', '0001_initial', 2026-05-19 18:19:12.658824);
INSERT INTO django_migrations (id, app, name, applied) VALUES (19, 'transactions', '0002_initial', 2026-05-19 18:19:12.660148);
INSERT INTO django_migrations (id, app, name, applied) VALUES (20, 'transactions', '0003_add_arrived_status', 2026-05-19 18:19:12.661662);
INSERT INTO django_migrations (id, app, name, applied) VALUES (21, 'admin', '0001_initial', 2026-05-19 18:35:46.517696);
INSERT INTO django_migrations (id, app, name, applied) VALUES (22, 'admin', '0002_logentry_remove_auto_add', 2026-05-19 18:35:46.522920);
INSERT INTO django_migrations (id, app, name, applied) VALUES (23, 'admin', '0003_logentry_add_action_flag_choices', 2026-05-19 18:35:46.528107);
INSERT INTO django_migrations (id, app, name, applied) VALUES (24, 'transactions', '0004_add_shipping_info', 2026-05-19 19:00:14.005254);
INSERT INTO django_migrations (id, app, name, applied) VALUES (25, 'sessions', '0001_initial', 2026-05-29 13:25:12.983271);
INSERT INTO django_migrations (id, app, name, applied) VALUES (26, 'users', '0002_alter_user_name', 2026-05-29 15:16:16.869152);
INSERT INTO django_migrations (id, app, name, applied) VALUES (27, 'users', '0003_alter_user_grade_alter_user_major_alter_user_name', 2026-05-29 15:16:17.269675);
INSERT INTO django_migrations (id, app, name, applied) VALUES (28, 'users', '0004_alter_user_student_id', 2026-05-29 15:16:17.285637);
INSERT INTO django_migrations (id, app, name, applied) VALUES (29, 'users', '0005_alter_user_name', 2026-05-29 15:16:17.554401);
