import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_trade.settings')
django.setup()

from user_accounts.models import User

# 检查是否存在名为"wj"的用户
users = User.objects.filter(name='wj')
print(f"找到 {users.count()} 个名为'wj'的用户")

if users.exists():
    # 删除用户
    users.delete()
    print("删除成功！")
else:
    print("用户不存在，无需删除")

# 检查是否存在学号重复的情况
from django.db.models import Count

# 统计重复的学号
duplicate_student_ids = User.objects.values('student_id').annotate(count=Count('student_id')).filter(count__gt=1)

if duplicate_student_ids.exists():
    print("存在重复的学号：")
    for item in duplicate_student_ids:
        print(f"学号: {item['student_id']}, 重复次数: {item['count']}")
else:
    print("所有学号都是唯一的")
