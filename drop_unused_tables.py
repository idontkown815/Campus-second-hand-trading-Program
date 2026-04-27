import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# 连接数据库
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='campus_trade',
    charset='utf8mb4'
)

try:
    with connection.cursor() as cursor:
        # 需要删除的表（Django 自带但未使用），按依赖顺序排列
        # 先删除子表，再删除父表
        tables_to_drop = [
            # 子表先删
            'users_groups',
            'users_user_permissions',
            'auth_group_permissions',
            'auth_permission',
            # Django 系统表
            'django_admin_log',
            'django_migrations',
            'django_session',
            'django_content_type',
            # 最后删父表
            'auth_group',
        ]

        # 删除不需要的表
        print("=" * 80)
        print("删除不需要的表（按依赖顺序）")
        print("=" * 80)

        for table in tables_to_drop:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
                print(f"✓ 已删除表: {table}")
            except Exception as e:
                print(f"✗ 删除表 {table} 失败: {e}")

        connection.commit()

        # 显示删除后的所有表
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("\n" + "=" * 80)
        print("删除后的所有表")
        print("=" * 80)
        for table in tables:
            print(f"  - {table[0]}")
        print(f"\n剩余表数: {len(tables)}")

finally:
    connection.close()
