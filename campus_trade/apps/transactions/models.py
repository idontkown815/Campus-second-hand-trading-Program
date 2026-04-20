from django.db import models
from django.conf import settings
from datetime import datetime, timedelta


class Transaction(models.Model):
    """交易模型"""
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='transactions', verbose_name="商品")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer_transactions', verbose_name="买家")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_transactions', verbose_name="卖家")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="状态")
    locked_until = models.DateTimeField(null=True, blank=True, verbose_name="锁定截止时间")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'transactions'
        verbose_name = '交易'
        verbose_name_plural = '交易'

    def save(self, *args, **kwargs):
        # 当交易状态变为已确认时，设置24小时锁定时间
        if self.status == 'confirmed' and not self.locked_until:
            self.locked_until = datetime.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
