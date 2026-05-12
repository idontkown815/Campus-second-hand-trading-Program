from rest_framework import serializers
from .models import Category, Product
from django.conf import settings


class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    """商品序列化器"""
    seller = serializers.StringRelatedField()
    seller_id = serializers.IntegerField(source='seller.id', read_only=True)
    images = serializers.SerializerMethodField()
    image_list = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    transaction_status = serializers.SerializerMethodField()
    buyer_id = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'seller_id', 'title', 'description', 'price', 'stock', 'category',
            'images', 'image_list', 'campus_location', 'building_location', 'status',
            'created_at', 'updated_at', 'transaction_status', 'buyer_id'
        ]

    def get_images(self, obj):
        """获取图片相对路径"""
        if not obj.images:
            return []

        images = obj.images.split(',') if isinstance(obj.images, str) else obj.images
        full_images = []
        for img in images:
            if isinstance(img, str):
                img = img.strip()
                if img:
                    full_images.append('/uploads/' + img)
        return full_images

    def get_transaction_status(self, obj):
        """获取交易状态用于显示"""
        from apps.transactions.models import Transaction
        try:
            transaction = Transaction.objects.filter(product=obj).exclude(
                status__in=['cancelled', 'expired']
            ).select_related('buyer', 'seller').first()
            if transaction:
                return transaction.status
        except Exception:
            pass
        return None

    def get_buyer_id(self, obj):
        """获取买家ID"""
        from apps.transactions.models import Transaction
        try:
            transaction = Transaction.objects.filter(product=obj).exclude(
                status__in=['cancelled', 'expired']
            ).select_related('buyer').first()
            if transaction:
                return transaction.buyer.id
        except Exception:
            pass
        return None

    def create(self, validated_data):
        image_list = validated_data.pop('image_list', [])
        if image_list:
            validated_data['images'] = image_list

        validated_data['seller'] = self.context['request'].user

        validated_data['status'] = 'available'

        return super().create(validated_data)

    def update(self, instance, validated_data):
        image_list = validated_data.pop('image_list', None)
        if image_list is not None:
            instance.images = image_list

        return super().update(instance, validated_data)