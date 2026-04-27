-- =====================================================
-- 校园二手交易平台 - MySQL 数据库设计文档
-- Campus Second-hand Trading Platform
-- =====================================================

-- 项目名称：校园二手交易平台
-- 数据库名称：campus_trade
-- MySQL 版本：8.0+
-- 字符集：utf8mb4
-- 生成日期：2026-04-27
-- =====================================================

-- =====================================================
-- 一、项目需要的表（共10张）
-- =====================================================

/*
┌─────────────────┬──────────────────────────────┐
│ 表名            │ 说明                          │
├─────────────────┼──────────────────────────────┤
│ users           │ 用户表                        │
│ categories      │ 商品分类表                     │
│ products        │ 商品表                        │
│ transactions    │ 交易表                        │
│ conversations   │ 会话表（私信）                 │
│ messages        │ 消息表                        │
│ favorites       │ 收藏表                        │
│ reports         │ 举报表                        │
│ blocks          │ 拉黑表                        │
│ conversations_  │ 会话参与者关联表（多对多）     │
│ participants    │                              │
└─────────────────┴──────────────────────────────┘
*/

-- =====================================================
-- 二、删除的表（共9张）
-- =====================================================

/*
┌─────────────────┬──────────────────────────────┐
│ 表名            │ 说明                          │
├─────────────────┼──────────────────────────────┤
│ auth_group              │ Django用户组表（未使用）    │
│ auth_group_permissions  │ Django组权限表（未使用）    │
│ auth_permission         │ Django权限表（未使用）      │
│ django_admin_log       │ Django管理日志（未使用）    │
│ django_content_type    │ Django内容类型（未使用）    │
│ django_migrations      │ Django迁移记录（可删除）    │
│ django_session         │ Django会话表（未使用）      │
│ users_groups           │ 用户组关系表（未使用）      │
│ users_user_permissions│ 用户权限关系表（未使用）    │
└─────────────────┴──────────────────────────────┘
*/

-- =====================================================
-- 三、表结构说明
-- =====================================================

-- 1. users 表 - 用户表
-- 说明：存储所有用户信息，继承自Django的AbstractUser
-- 关联：与products（卖家）、transactions（买家/卖家）、
--       conversations（参与者）、messages（发送者）、
--       favorites、reports（举报人/被举报人）、blocks（拉黑者/被拉黑者）关联

-- 2. categories 表 - 商品分类表
-- 说明：存储商品分类信息
-- 关联：被products表引用

-- 3. products 表 - 商品表
-- 说明：存储商品信息，包括标题、描述、价格、图片等
-- 关联：与users（卖家）、conversations、transactions、favorites、reports关联

-- 4. transactions 表 - 交易表
-- 说明：存储交易记录，包括状态和锁定时间
-- 关联：与products、users（买家和卖家）关联

-- 5. conversations 表 - 会话表
-- 说明：存储用户之间的私信会话
-- 关联：与users（参与者）、products、messages关联
-- 注意：通过conversations_participants中间表实现多对多关系

-- 6. messages 表 - 消息表
-- 说明：存储会话中的消息
-- 关联：与conversations、users（发送者）关联

-- 7. favorites 表 - 收藏表
-- 说明：存储用户的商品收藏
-- 关联：与users、products关联
-- 注意：(user_id, product_id)唯一，避免重复收藏

-- 8. reports 表 - 举报表
-- 说明：存储用户举报记录
-- 关联：与users（举报人和被举报人）、products关联

-- 9. blocks 表 - 拉黑表
-- 说明：存储用户拉黑记录
-- 关联：与users（拉黑者和被拉黑者）关联
-- 注意：(blocker_id, blocked_id)唯一，避免重复拉黑

-- 10. conversations_participants 表 - 会话参与者关联表
-- 说明：Django自动创建的多对多中间表
-- 关联：conversations和users的多对多关系

-- =====================================================
-- 四、表关系图
-- =====================================================

/*
                        users
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
      products       conversations      blocks
          │               │               │
          ▼               │               │
      favorites          │               │
          │               ▼               │
          │           messages            │
          │               │               │
          ▼               ▼               │
      reports            │               │
          │               │               │
          └───────────┬───┘               │
                      │                   │
                      ▼                   │
                 transactions            │
                      │                   │
                      └───────────────────┘
*/

-- =====================================================
-- 五、使用说明
-- =====================================================

/*
1. 执行顺序：
   首先执行 users.sql（因为其他表依赖它）
   然后按顺序执行其他表

2. 或者直接导入完整的SQL文件：
   mysql -u root -p campus_trade < init_database.sql

3. 注意事项：
   - 所有表使用 InnoDB 引擎，支持事务和外键
   - 字符集使用 utf8mb4，支持emoji等特殊字符
   - 外键约束确保数据完整性
   - 建议定期备份数据库
*/

-- =====================================================
-- 六、相关文件列表
-- =====================================================

/*
01_users.sql          - 用户表
02_categories.sql     - 商品分类表
03_products.sql       - 商品表
04_transactions.sql   - 交易表
05_conversations.sql  - 会话表
06_messages.sql       - 消息表
07_favorites.sql      - 收藏表
08_reports.sql        - 举报表
09_blocks.sql         - 拉黑表
10_conversations_participants.sql - 会话参与者关联表
*/
