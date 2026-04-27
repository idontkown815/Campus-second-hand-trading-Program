import os
import sys
import django

sys.path.insert(0, r'd:\pbl6\Project\campus_trade')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_trade.settings')
django.setup()

from django.test import RequestFactory
from rest_framework.request import Request
from apps.products.models import Product
from apps.products.serializers import ProductSerializer

print('=' * 80)
print('完整图片流程测试')
print('=' * 80)

# 模拟一个真实请求
factory = RequestFactory()
request = factory.get('/')
request.user = None  # 模拟未认证用户

ctx = {'request': Request(request)}

# 测试场景1: images 是空列表
print('\n场景1: images 是空列表')
p1 = Product(id=99, title='Test', description='Desc', price=100,
             campus_location='成都校区', building_location='1栋',
             images=[], seller_id=1)
s1 = ProductSerializer(p1, context=ctx)
print(f'  原始: {p1.images}')
print(f'  序列化: {s1.data.get("images")}')

# 测试场景2: images 是包含文件名的列表
print('\n场景2: images 是列表 ["test.jpg"]')
p2 = Product(id=99, title='Test', description='Desc', price=100,
             campus_location='成都校区', building_location='1栋',
             images=['test.jpg'], seller_id=1)
s2 = ProductSerializer(p2, context=ctx)
print(f'  原始: {p2.images}')
print(f'  序列化: {s2.data.get("images")}')

# 测试场景3: images 是逗号分隔的字符串 (旧格式)
print('\n场景3: images 是字符串 "test1.jpg,test2.jpg"')
p3 = Product(id=99, title='Test', description='Desc', price=100,
             campus_location='成都校区', building_location='1栋',
             images='test1.jpg,test2.jpg', seller_id=1)
s3 = ProductSerializer(p3, context=ctx)
print(f'  原始: {p3.images}')
print(f'  序列化: {s3.data.get("images")}')

# 测试场景4: images 包含带路径的文件名
print('\n场景4: images 是列表包含 "/uploads/test.jpg"')
p4 = Product(id=99, title='Test', description='Desc', price=100,
             campus_location='成都校区', building_location='1栋',
             images=['/uploads/test.jpg'], seller_id=1)
s4 = ProductSerializer(p4, context=ctx)
print(f'  原始: {p4.images}')
print(f'  序列化: {s4.data.get("images")}')

print('\n' + '=' * 80)
print('问题分析')
print('=' * 80)
print('''
从测试结果可以看出:
1. 当 images 是列表时，会正确添加 /uploads/ 前缀
2. 当 images 是字符串时，会先 split 成列表再处理

可能的问题来源:
1. 数据库中的 images 字段为空 (已验证，多个产品 images=[])
2. 前端上传时没有正确保存图片文件名到 form.image_list
3. 前端上传后响应处理不正确

需要检查:
1. handleUploadSuccess 是否正确从 response 中提取 url
2. 后端 upload 接口是否正确返回 {code: 200, data: {url: filename}}
3. createProduct 时是否正确传递 image_list 参数
''')
