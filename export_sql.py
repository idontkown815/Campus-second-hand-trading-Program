import os
import pymysql

# 数据库连接配置
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'campus_trade',
    'port': 3306,
    'charset': 'utf8mb4'
}

# 输出目录
output_dir = r'd:\pbl6\Project\Campus-second-hand-trading-Program\mysql数据表'

def export_tables():
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 连接数据库
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # 获取所有表名
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"发现 {len(tables)} 个表")
        
        for (table_name,) in tables:
            # 获取表结构
            cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
            result = cursor.fetchone()
            create_table_sql = result[1]
            
            # 生成SQL文件
            sql_file_path = os.path.join(output_dir, f"{table_name}.sql")
            with open(sql_file_path, 'w', encoding='utf-8') as f:
                f.write(f"-- 表: {table_name}\n")
                f.write(create_table_sql)
                f.write(";\n")
            
            print(f"已导出: {table_name}.sql")
        
        print("\n所有表导出完成！")
        
    except Exception as e:
        print(f"导出失败: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    export_tables()
