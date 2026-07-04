import pymysql
import os

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'campus_trade',
    'charset': 'utf8mb4'
}

def drop_all_tables():
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"Dropping table: {table_name}")
            cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
        
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        conn.commit()
        print("All tables dropped successfully!")
        
    finally:
        cursor.close()
        conn.close()

def import_sql_files():
    sql_dir = r'd:\three2\PBL6\idontknow\Campus-second-hand-trading-Program\mysql数据表'
    
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        
        import_order = [
            'django_content_type.sql',
            'auth_permission.sql',
            'auth_group.sql',
            'auth_group_permissions.sql',
            'users.sql',
            'users_groups.sql',
            'users_user_permissions.sql',
            'addresses.sql',
            'blocks.sql',
            'categories.sql',
            'products.sql',
            'comments.sql',
            'favorites.sql',
            'reports.sql',
            'transactions.sql',
            'conversations.sql',
            'messages.sql',
            'conversations_participants.sql',
            'django_admin_log.sql',
            'django_migrations.sql',
            'django_session.sql'
        ]
        
        for sql_file in import_order:
            file_path = os.path.join(sql_dir, sql_file)
            print(f"Importing: {sql_file}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            statements = sql_content.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)
            
            conn.commit()
        
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        print("All SQL files imported successfully!")
        
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("=== Dropping all tables ===")
    drop_all_tables()
    
    print("\n=== Importing SQL files ===")
    import_sql_files()
    
    print("\n=== Database reset completed ===")
