import pymysql

# 数据库连接配置
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'campus_trade',
    'charset': 'utf8mb4'
}

try:
    # 连接数据库
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    
    # 查看引用 users 表的外键约束
    cursor.execute("""
        SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE REFERENCED_TABLE_NAME = 'users' AND TABLE_SCHEMA = 'campus_trade'
    """)
    foreign_keys = cursor.fetchall()
    
    print("引用 users 表的外键约束:")
    for fk in foreign_keys:
        print(f"表: {fk[0]}, 字段: {fk[1]}, 约束名: {fk[2]}")
    
    # 删除外键约束
    for fk in foreign_keys:
        table_name = fk[0]
        constraint_name = fk[2]
        try:
            cursor.execute(f"ALTER TABLE {table_name} DROP FOREIGN KEY {constraint_name}")
            print(f"已删除外键约束 {constraint_name}")
        except Exception as e:
            print(f"删除外键约束 {constraint_name} 时出错: {e}")
    
    # 删除表
    tables_to_delete = ['users', 'users_groups', 'users_groups_permissions']
    
    for table in tables_to_delete:
        try:
            cursor.execute(f"SHOW TABLES LIKE '{table}'")
            result = cursor.fetchone()
            
            if result:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"表 {table} 删除成功")
            else:
                print(f"表 {table} 不存在")
        except Exception as e:
            print(f"删除表 {table} 时出错: {e}")
    
    conn.commit()
    print("\n所有操作已提交")
    
except Exception as e:
    print(f"数据库操作失败: {e}")
finally:
    if 'conn' in locals() and conn.open:
        cursor.close()
        conn.close()
        print("数据库连接已关闭")