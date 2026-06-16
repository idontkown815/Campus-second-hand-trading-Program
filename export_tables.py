import os
import sys
import mysql.connector

# 设置默认编码
sys.stdout.reconfigure(encoding='utf-8')

# 数据库配置
config = {
    'user': 'root',
    'password': '123456',
    'host': 'localhost',
    'database': 'campus_trade',
    'charset': 'utf8mb4'
}

# 输出目录
output_dir = r'd:\three2\PBL6\idontknow\Campus-second-hand-trading-Program\mysql数据表'

try:
    # 连接数据库
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    print("Connected to database successfully!")
    
    # 获取所有表名
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\nFound {len(tables)} tables:")
    for table in tables:
        print(f"  - {table}")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 逐个导出表
    for table in tables:
        file_path = os.path.join(output_dir, f"{table}.sql")
        print(f"\nExporting {table}...")
        
        # 获取表结构
        cursor.execute(f"SHOW CREATE TABLE {table}")
        create_table_sql = cursor.fetchone()[1]
        
        # 获取表数据
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        
        # 获取列名
        cursor.execute(f"DESCRIBE {table}")
        columns = [col[0] for col in cursor.fetchall()]
        
        # 生成INSERT语句
        insert_statements = []
        if rows:
            for row in rows:
                values = []
                for val in row:
                    if val is None:
                        values.append('NULL')
                    elif isinstance(val, str):
                        # 转义特殊字符
                        escaped_val = val.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
                        values.append(f"'{escaped_val}'")
                    elif isinstance(val, bytes):
                        values.append(f"0x{val.hex()}")
                    else:
                        values.append(str(val))
                insert_statements.append(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)});")
        
        # 写入SQL文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"-- Table: {table}\n")
            f.write(f"{create_table_sql};\n\n")
            for insert in insert_statements:
                f.write(f"{insert}\n")
        
        print(f"  OK: {file_path}")
    
    print("\n✅ All tables exported successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
finally:
    if conn:
        conn.close()
