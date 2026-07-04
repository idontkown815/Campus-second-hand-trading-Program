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
    
    # 检查表是否存在
    cursor.execute("SHOW TABLES LIKE 'users_user_permissions'")
    result = cursor.fetchone()
    
    if result:
        # 尝试删除表
        cursor.execute("DROP TABLE IF EXISTS users_user_permissions")
        print("表 users_user_permissions 删除成功")
    else:
        print("表 users_user_permissions 不存在")
    
    conn.commit()
    print("操作已提交")
    
except Exception as e:
    print(f"数据库操作失败: {e}")
finally:
    if 'conn' in locals() and conn.open:
        cursor.close()
        conn.close()
        print("数据库连接已关闭")