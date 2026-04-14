from django.db import models
from user_accounts.models import User

class Category(models.Model):
    """商品分类"""
    name = models.CharField(max_length=100, unique=True, verbose_name='分类名称')
    description = models.TextField(blank=True, null=True, verbose_name='分类描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """商品模型"""
    # 商品状态
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('pending', '待审核'),
        ('active', '在售'),
        ('locked', '锁定中(预定)'),
        ('sold', '已售出'),
        ('removed', '已下架/违规'),
    )
    
    # 基本信息
    title = models.CharField(max_length=200, verbose_name='商品标题')
    description = models.TextField(verbose_name='商品描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    
    # 图片
    image1 = models.ImageField(upload_to='products/', verbose_name='图片1')
    image2 = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='图片2')
    image3 = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='图片3')
    
    # 位置信息
    campus = models.CharField(max_length=100, verbose_name='校区')
    building = models.CharField(max_length=100, blank=True, null=True, verbose_name='楼栋')
    
    # 状态
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    
    # 关联信息
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name='卖家')
    
    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    locked_until = models.DateTimeField(blank=True, null=True, verbose_name='锁定截止时间')
    
    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
    
    def __str__(self):
        return self.title

class Favorite(models.Model):
    """商品收藏"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='用户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='商品')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')
    
    class Meta:
        verbose_name = '商品收藏'
        verbose_name_plural = '商品收藏'
        unique_together = ('user', 'product')
    
    def __str__(self):
        return f'{self.user.username} 收藏 {self.product.title}'
