from rest_framework import serializers
from .models import Conversation, Message, Favorite, Report, Block


class MessageSerializer(serializers.ModelSerializer):
    """消息序列化器"""
    sender = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'is_read', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    """会话序列化器"""
    participants = serializers.StringRelatedField(many=True)
    product = serializers.StringRelatedField()
    last_message = MessageSerializer()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'product', 'last_message', 'created_at', 'updated_at']


class FavoriteSerializer(serializers.ModelSerializer):
    """收藏序列化器"""
    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product', 'created_at']


class ReportSerializer(serializers.ModelSerializer):
    """举报序列化器"""
    reporter = serializers.StringRelatedField()
    reported_user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()

    class Meta:
        model = Report
        fields = ['id', 'reporter', 'reported_user', 'product', 'reason', 'created_at']


class BlockSerializer(serializers.ModelSerializer):
    """拉黑序列化器"""
    blocker = serializers.StringRelatedField()
    blocked = serializers.StringRelatedField()

    class Meta:
        model = Block
        fields = ['id', 'blocker', 'blocked', 'created_at']
