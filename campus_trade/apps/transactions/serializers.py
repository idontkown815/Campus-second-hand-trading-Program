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
            'locked_until', 'locked_remaining_seconds', 'created_at', 'updated_at',
            'recipient_name', 'recipient_phone', 'shipping_address'
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
            if not product or not hasattr(product, 'images') or not product.images:
                return []
            
            images = []
            
            # 处理字符串格式（可能是 JSON 字符串）
            if isinstance(product.images, str):
                try:
                    import json
                    images = json.loads(product.images)
                except json.JSONDecodeError:
                    # 如果不是有效 JSON，尝试按逗号分割
                    images = product.images.split(',')
            elif isinstance(product.images, list):
                images = product.images
            
            # 构建完整的图片URL
            result = []
            for img in images:
                if img:
                    img_str = str(img).strip()
                    if img_str:
                        if img_str.startswith('http'):
                            result.append(img_str)
                        else:
                            # 添加正确的路径前缀
                            if not img_str.startswith('商品/'):
                                img_str = '商品/' + img_str
                            result.append('/uploads/' + img_str)
            
            return result
        except Exception as e:
            print(f"Error getting product images: {e}")
            return []
