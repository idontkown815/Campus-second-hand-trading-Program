from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """交易序列化器"""
    product = serializers.StringRelatedField()
    buyer = serializers.StringRelatedField()
    seller = serializers.StringRelatedField()
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_images = serializers.SerializerMethodField()
    buyer_id = serializers.IntegerField(source='buyer.id', read_only=True)
    seller_id = serializers.IntegerField(source='seller.id', read_only=True)
    locked_remaining_seconds = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'id', 'product', 'product_id', 'product_title', 'product_price', 'product_images',
            'buyer', 'buyer_id', 'seller', 'seller_id', 'status',
            'locked_until', 'locked_remaining_seconds', 'created_at', 'updated_at'
        ]

    def get_locked_remaining_seconds(self, obj):
        """计算剩余锁定时间（秒）"""
        if obj.locked_until:
            from django.utils import timezone
            remaining = (obj.locked_until - timezone.now()).total_seconds()
            return max(0, int(remaining))
        return 0

    def get_product_images(self, obj):
        """获取商品图片列表"""
        try:
            product = obj.product
            if product and hasattr(product, 'images') and product.images:
                images = product.images if isinstance(product.images, list) else []
                return ['/uploads/' + str(img) if img and not str(img).startswith('http') else str(img) for img in images if img]
            return []
        except Exception:
            return []
