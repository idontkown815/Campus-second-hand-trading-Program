from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    """商品序列化器"""
    seller = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'title', 'description', 'price', 'stock', 'category',
            'images', 'campus_location', 'building_location', 'status',
            'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        # 设置卖家为当前用户
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)
