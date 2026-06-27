from rest_framework import serializers
from .models import Conversation, Message, Favorite, Report, Block, Comment


class ProductSummarySerializer(serializers.ModelSerializer):
    """商品摘要序列化器"""
    images = serializers.SerializerMethodField()

    class Meta:
        from apps.products.models import Product
        model = Product
        fields = ['id', 'title', 'price', 'images']

    def get_images(self, obj):
        """获取图片完整URL"""
        if not obj.images:
            return []

        import json
        images = []
        
        if isinstance(obj.images, str):
            try:
                images = json.loads(obj.images)
            except json.JSONDecodeError:
                images = obj.images.split(',')
        else:
            images = obj.images
        
        full_images = []
        request = self.context.get('request')
        for img in images:
            if isinstance(img, str):
                img = img.strip()
                if img:
                    # 图片存储在 /uploads/商品/ 目录下
                    img_path = img
                    if not img_path.startswith('商品/'):
                        img_path = '商品/' + img_path
                    if request:
                        full_url = request.build_absolute_uri('/uploads/' + img_path)
                    else:
                        full_url = '/uploads/' + img_path
                    full_images.append(full_url)
        return full_images


class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Comment._meta.get_field('product').related_model.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_id', 'product', 'content', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """消息序列化器"""
    sender = serializers.StringRelatedField(read_only=True)
    sender_id = serializers.SerializerMethodField()
    conversation = serializers.PrimaryKeyRelatedField(queryset=Message._meta.get_field('conversation').related_model.objects.all(), write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_id', 'conversation', 'content', 'is_read', 'created_at']

    def get_sender_id(self, obj):
        return obj.sender.id if obj.sender else None


class ConversationSerializer(serializers.ModelSerializer):
    """会话序列化器"""
    participants = serializers.SerializerMethodField()
    product = ProductSummarySerializer()
    last_message = MessageSerializer(allow_null=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'product', 'last_message', 'created_at', 'updated_at']

    def get_participants(self, obj):
        return [{'id': p.id, 'name': str(p)} for p in obj.participants.all()]


class FavoriteSerializer(serializers.ModelSerializer):
    """收藏序列化器"""
    user = serializers.StringRelatedField(read_only=True)
    product = ProductSummarySerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product', 'product_id', 'created_at']


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
