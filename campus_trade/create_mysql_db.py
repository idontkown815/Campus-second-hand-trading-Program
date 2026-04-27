import pymysql

# 连接到MySQL服务器（不指定数据库）
try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        port=3306,
        charset='utf8mb4'
    )
    
    # 创建游标
    cursor = conn.cursor()
    
    # 创建数据库
    cursor.execute("CREATE DATABASE IF NOT EXISTS campus_trade CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print("数据库创建成功")
    
    # 关闭游标和连接
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"创建数据库时出错: {e}")
