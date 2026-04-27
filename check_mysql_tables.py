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
        # 显示所有表
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("=" * 80)
        print("MySQL 数据库中的所有表")
        print("=" * 80)
        for table in tables:
            print(f"  - {table[0]}")
        print(f"\n总表数: {len(tables)}")
        
finally:
    connection.close()
