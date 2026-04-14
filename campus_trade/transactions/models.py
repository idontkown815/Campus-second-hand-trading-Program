from django.db import models
from user_accounts.models import User
from products.models import Product

class Transaction(models.Model):
    """交易模型"""
    # 交易状态
    STATUS_CHOICES = (
        ('pending', '待确认'),
        ('locked', '已锁定'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )
    
    # 关联信息
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases', verbose_name='买家')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales', verbose_name='卖家')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions', verbose_name='商品')
    
    # 交易信息
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='交易价格')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    
    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name='完成时间')
    
    class Meta:
        verbose_name = '交易'
        verbose_name_plural = '交易'
    
    def __str__(self):
        return f'{self.buyer.username} 购买 {self.product.title}'

class TransactionHistory(models.Model):
    """交易历史"""
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='history', verbose_name='交易')
    status = models.CharField(max_length=20, choices=Transaction.STATUS_CHOICES, verbose_name='状态')
    message = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '交易历史'
        verbose_name_plural = '交易历史'
    
    def __str__(self):
        return f'{self.transaction} - {self.status}'
