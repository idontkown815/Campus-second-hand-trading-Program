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

    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'seller_id', 'title', 'description', 'price', 'stock', 'category',
            'images', 'image_list', 'campus_location', 'building_location', 'status',
            'created_at', 'updated_at'
        ]

    def get_images(self, obj):
        """获取图片相对路径"""
        if not obj.images:
            return []
        
        # 处理图片列表，返回相对路径
        images = obj.images.split(',') if isinstance(obj.images, str) else obj.images
        full_images = []
        for img in images:
            # 确保img是字符串
            if isinstance(img, str):
                img = img.strip()
                if img:
                    # 直接返回相对路径，前端会通过Vite代理访问
                    full_images.append('/uploads/' + img)
        return full_images

    def create(self, validated_data):
        # 处理图片列表
        image_list = validated_data.pop('image_list', [])
        if image_list:
            validated_data['images'] = image_list
        
        # 设置卖家为当前用户
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # 处理图片列表
        image_list = validated_data.pop('image_list', None)
        if image_list is not None:
            instance.images = image_list
        
        return super().update(instance, validated_data)
