import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_trade.settings')
django.setup()

from user_accounts.models import User

# 检查是否已存在超级用户
if not User.objects.filter(username='admin').exists():
    # 创建超级用户
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print('超级用户创建成功！')
else:
    print('超级用户已存在！')
