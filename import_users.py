import sqlite3
import pymysql

# 连接SQLite数据库
sqlite_conn = sqlite3.connect(r'd:\three2\PBL6\idontknow\Campus-second-hand-trading-Program\campus_trade\db.sqlite3')
sqlite_cursor = sqlite_conn.cursor()

# 连接MySQL数据库
mysql_conn = pymysql.connect(host='localhost', user='root', password='123456', database='campus_trade')
mysql_cursor = mysql_conn.cursor()

# 获取SQLite中的所有用户
sqlite_cursor.execute('SELECT * FROM users')
users = sqlite_cursor.fetchall()

print(f'从SQLite读取到 {len(users)} 个用户')

# SQLite列顺序: id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, student_id, grade, major, avatar, name, gender

# 禁用外键检查
mysql_cursor.execute("SET FOREIGN_KEY_CHECKS=0")

# 先删除MySQL中现有的用户（保留管理员）
mysql_cursor.execute("DELETE FROM users WHERE student_id != '00000000'")
mysql_conn.commit()
print('已清除MySQL中的旧用户数据（保留管理员）')

# 导入用户数据
for user in users:
    # SQLite列顺序
    id_val = user[0]
    password = user[1]
    last_login = user[2]
    is_superuser = user[3]
    username = user[4]
    first_name = user[5]
    last_name = user[6]
    email = user[7]
    is_staff = user[8]
    is_active = user[9]
    date_joined = user[10]
    student_id = user[11]
    grade = user[12] if user[12] else ''
    major = user[13] if user[13] else ''
    avatar = user[14]
    name = user[15] if user[15] else username
    gender = user[16]
    
    # 检查是否已存在（管理员）
    mysql_cursor.execute("SELECT id FROM users WHERE student_id = %s", (student_id,))
    if mysql_cursor.fetchone():
        print(f'跳过已存在的用户: {username} (学号: {student_id})')
        continue
    
    # 插入用户
    sql = '''
    INSERT INTO users (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, name, student_id, grade, major, avatar, gender)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    mysql_cursor.execute(sql, (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, name, student_id, grade, major, avatar, gender))
    print(f'导入用户: {username} (学号: {student_id}, 姓名: {name})')

mysql_conn.commit()

# 重新启用外键检查
mysql_cursor.execute("SET FOREIGN_KEY_CHECKS=1")
print('\n用户导入完成！')

# 验证导入结果
mysql_cursor.execute('SELECT id, username, student_id, name, is_superuser, is_staff, is_active FROM users')
result = mysql_cursor.fetchall()
print(f'\nMySQL数据库中现有用户数量: {len(result)}')
for u in result:
    print(f'  ID:{u[0]}, 用户名:{u[1]}, 学号:{u[2]}, 姓名:{u[3]}, super:{u[4]}, staff:{u[5]}, active:{u[6]}')

sqlite_cursor.close()
sqlite_conn.close()
mysql_cursor.close()
mysql_conn.close()