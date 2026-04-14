from django.db import models
from user_accounts.models import User
from products.models import Product

class Conversation(models.Model):
    """会话模型"""
    # 关联信息
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='conversations', verbose_name='商品')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_conversations', verbose_name='买家')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_conversations', verbose_name='卖家')
    
    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '会话'
        verbose_name_plural = '会话'
        unique_together = ('product', 'buyer', 'seller')
    
    def __str__(self):
        return f'{self.buyer.username} 与 {self.seller.username} 关于 {self.product.title} 的会话'

class Message(models.Model):
    """消息模型"""
    # 关联信息
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name='会话')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='发送者')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name='接收者')
    
    # 消息内容
    content = models.TextField(verbose_name='消息内容')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    
    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')
    
    class Meta:
        verbose_name = '消息'
        verbose_name_plural = '消息'
        ordering = ['created_at']
    
    def __str__(self):
        return f'{self.sender.username} 发送给 {self.receiver.username} 的消息'

class Block(models.Model):
    """拉黑模型"""
    # 关联信息
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users', verbose_name='用户')
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by', verbose_name='被拉黑用户')
    
    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='拉黑时间')
    
    class Meta:
        verbose_name = '拉黑'
        verbose_name_plural = '拉黑'
        unique_together = ('user', 'blocked_user')
    
    def __str__(self):
        return f'{self.user.username} 拉黑了 {self.blocked_user.username}'

class Report(models.Model):
    """举报模型"""
    # 举报类型
    REPORT_TYPE_CHOICES = (
        ('spam', '垃圾信息'),
        ('scam', '诈骗'),
        ('inappropriate', '不当内容'),
        ('other', '其他'),
    )
    
    # 关联信息
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports', verbose_name='举报者')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_by', verbose_name='被举报用户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='reports', verbose_name='相关商品')
    
    # 举报信息
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, verbose_name='举报类型')
    description = models.TextField(verbose_name='举报描述')
    is_processed = models.BooleanField(default=False, verbose_name='是否已处理')
    
    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='举报时间')
    processed_at = models.DateTimeField(blank=True, null=True, verbose_name='处理时间')
    
    class Meta:
        verbose_name = '举报'
        verbose_name_plural = '举报'
    
    def __str__(self):
        return f'{self.reporter.username} 举报了 {self.reported_user.username}'
