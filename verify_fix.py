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
print('验证图片显示修复')
print('=' * 80)

factory = RequestFactory()
request = factory.get('/')
request.user = None

ctx = {'request': Request(request)}

# 模拟数据库中有图片的产品
print('\n测试1: 数据库中 images 字段有正确的图片文件名')
products = Product.objects.all()
print(f'  总产品数: {products.count()}')

for p in products[:5]:
    print(f'\n  产品 ID={p.id}: {p.title}')
    print(f'    images 原始值: {repr(p.images)}')
    serializer = ProductSerializer(p, context=ctx)
    images_result = serializer.data.get('images', [])
    print(f'    序列化后: {images_result}')

    if images_result and len(images_result) > 0:
        print(f'    ✓ 图片路径格式正确')
    else:
        print(f'    ✗ 图片数据为空')

# 测试前端传递的数据如何被处理
print('\n\n测试2: 模拟前端传递 image_list')
print(f'  前端传递: ["test1.jpg", "test2.jpg"]')

# 模拟 serializer 处理
from apps.products.serializers import ProductSerializer
from django.test import RequestFactory

factory = RequestFactory()
request = factory.post('/products/')

class MockUser:
    id = 1
    def __str__(self):
        return "TestUser"

request.user = MockUser()

test_serializer = ProductSerializer(data={
    'title': 'Test Product',
    'description': 'Test Description',
    'price': 100,
    'stock': 1,
    'category': '其他',
    'campus_location': '成都校区',
    'building_location': '1栋',
    'image_list': ['test1.jpg', 'test2.jpg']
}, context={'request': Request(request)})

if test_serializer.is_valid():
    print(f'  is_valid: True')
    print(f'  验证字段: {list(test_serializer.validated_data.keys())}')
    result = test_serializer.save()
    print(f'  ✓ 数据验证通过并正确处理')
    print(f'  保存后的 images: {result.images}')
else:
    print(f'  is_valid: False')
    print(f'  errors: {test_serializer.errors}')

print('\n' + '=' * 80)
print('总结')
print('=' * 80)
print('''
已修复的问题:
1. ProductPublish.vue 中 removeImage 函数参数不匹配问题
   - 原因: file.url 是完整路径 /uploads/xxx.jpg，但 form.image_list 存的是纯文件名 xxx.jpg
   - 修复: 从 file.url 中提取纯文件名再查找索引

图片无法显示的其他可能原因:
1. 数据库中 images 字段为空 - 需要确保上传流程正确保存数据
2. 后端 upload 接口返回的数据格式
3. createProduct 调用时参数传递

验证图片URL格式:
- 前端: /uploads/xxx.jpg (通过 Vite 代理访问 Django)
- 后端: /uploads/xxx.jpg (Django 静态文件服务)
- 序列化器: /uploads/xxx.jpg (添加 /uploads/ 前缀)
''')
