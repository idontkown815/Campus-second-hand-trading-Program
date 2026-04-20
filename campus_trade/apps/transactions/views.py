from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """交易视图"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # 只返回当前用户相关的交易
        queryset = Transaction.objects.filter(
            models.Q(buyer=request.user) | models.Q(seller=request.user)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        # 创建交易意向
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 200,
                'message': '创建成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': 400,
            'message': '创建失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def confirm_transaction(self, request, pk=None):
        # 确认交易
        try:
            transaction = Transaction.objects.get(pk=pk)
            if transaction.seller == request.user:
                transaction.status = 'confirmed'
                transaction.save()
                return Response({
                    'code': 200,
                    'message': '确认成功',
                    'data': self.get_serializer(transaction).data
                })
            return Response({
                'code': 403,
                'message': '只有卖家可以确认交易'
            }, status=status.HTTP_403_FORBIDDEN)
        except Transaction.DoesNotExist:
            return Response({
                'code': 404,
                'message': '交易不存在'
            }, status=status.HTTP_404_NOT_FOUND)
