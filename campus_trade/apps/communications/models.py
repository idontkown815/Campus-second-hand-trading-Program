from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """会话模型"""
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations', verbose_name="参与者")
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='conversations', verbose_name="商品")
    last_message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="最后一条消息")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'conversations'
        verbose_name = '会话'
        verbose_name_plural = '会话'


class Message(models.Model):
    """消息模型"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name="会话")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="发送者")
    content = models.TextField(max_length=1000, verbose_name="内容")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")

    class Meta:
        db_table = 'messages'
        verbose_name = '消息'
        verbose_name_plural = '消息'


class Favorite(models.Model):
    """收藏模型"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites', verbose_name="用户")
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='favorites', verbose_name="商品")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")

    class Meta:
        db_table = 'favorites'
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        unique_together = ('user', 'product')


class Report(models.Model):
    """举报模型"""
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports', verbose_name="举报人")
    reported_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported', verbose_name="被举报人")
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reports', verbose_name="相关商品")
    reason = models.TextField(max_length=500, verbose_name="举报原因")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="举报时间")

    class Meta:
        db_table = 'reports'
        verbose_name = '举报'
        verbose_name_plural = '举报'


class Block(models.Model):
    """拉黑模型"""
    blocker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blocking', verbose_name="拉黑者")
    blocked = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blocked_by', verbose_name="被拉黑者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="拉黑时间")

    class Meta:
        db_table = 'blocks'
        verbose_name = '拉黑'
        verbose_name_plural = '拉黑'
        unique_together = ('blocker', 'blocked')
