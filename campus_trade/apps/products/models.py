from django.db import models
from django.conf import settings


class Category(models.Model):
    """商品分类"""
    name = models.CharField(max_length=50, verbose_name="分类名称")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 'categories'
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name


class Product(models.Model):
    """商品模型"""
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('available', '在售'),
        ('locked', '锁定中'),
        ('sold', '已售出'),
        ('rejected', '已下架'),
    ]

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products', verbose_name="卖家")
    title = models.CharField(max_length=100, verbose_name="标题")
    description = models.TextField(max_length=2000, verbose_name="描述")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="分类")
    images = models.JSONField(default=list, verbose_name="图片列表")
    campus_location = models.CharField(max_length=100, verbose_name="校区位置")
    building_location = models.CharField(max_length=100, verbose_name="楼栋位置")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="状态")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'products'
        verbose_name = '商品'
        verbose_name_plural = '商品'

    def __str__(self):
        return self.title
