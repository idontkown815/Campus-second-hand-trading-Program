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

# 输出文件夹
output_dir = r"d:\pbl6\Project\mysql数据表"

# 需要导出的表
tables_to_export = [
    'users',
    'categories',
    'products',
    'transactions',
    'conversations',
    'messages',
    'favorites',
    'reports',
    'blocks'
]

try:
    with connection.cursor() as cursor:
        print("=" * 80)
        print("导出 MySQL 建表语句")
        print("=" * 80)

        for table in tables_to_export:
            try:
                # 获取建表语句
                cursor.execute(f"SHOW CREATE TABLE `{table}`")
                result = cursor.fetchone()

                if result:
                    table_name = result[0]
                    create_statement = result[1]

                    # 写入文件
                    file_path = os.path.join(output_dir, f"{table_name}.sql")
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"-- MySQL 建表语句 for table `{table_name}`\n")
                        f.write(f"-- Generated at: 2026-04-27\n\n")
                        f.write(create_statement)
                        f.write(";\n")

                    print(f"✓ 已导出: {table_name}.sql")

            except Exception as e:
                print(f"✗ 导出表 {table} 失败: {e}")

        # 导出关联表 conversations_participants
        try:
            cursor.execute("SHOW CREATE TABLE `conversations_participants`")
            result = cursor.fetchone()
            if result:
                table_name = result[0]
                create_statement = result[1]
                file_path = os.path.join(output_dir, f"{table_name}.sql")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"-- MySQL 建表语句 for table `{table_name}`\n")
                    f.write(f"-- Generated at: 2026-04-27\n\n")
                    f.write(create_statement)
                    f.write(";\n")
                print(f"✓ 已导出: {table_name}.sql")
        except Exception as e:
            print(f"✗ 导出表 conversations_participants 失败: {e}")

    print("\n" + "=" * 80)
    print("导出完成！文件保存在: " + output_dir)
    print("=" * 80)

finally:
    connection.close()
