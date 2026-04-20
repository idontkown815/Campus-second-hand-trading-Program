from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """交易序列化器"""
    product = serializers.StringRelatedField()
    buyer = serializers.StringRelatedField()
    seller = serializers.StringRelatedField()

    class Meta:
        model = Transaction
        fields = [
            'id', 'product', 'buyer', 'seller', 'status',
            'locked_until', 'created_at', 'updated_at'
        ]
