from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Transaction
from .serializers import TransactionSerializer
from apps.products.models import Product


class TransactionViewSet(viewsets.ModelViewSet):
    """交易视图"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """获取当前用户相关的所有交易"""
        try:
            queryset = Transaction.objects.filter(
                models.Q(buyer=request.user) | models.Q(seller=request.user)
            ).select_related('product', 'buyer', 'seller').order_by('-created_at')

            # 更新商品锁定状态
            for transaction in queryset:
                try:
                    if transaction.product and not transaction.product.is_deleted:
                        transaction.product.check_and_update_lock_status()
                except Exception:
                    pass

            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            import logging
            logger = logging.getLogger('django')
            logger.error(f"获取交易列表失败: {str(e)}")
            return Response({
                'code': 500,
                'message': f'获取失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        """创建交易意向（购买意向）"""
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({
                'code': 400,
                'message': '商品ID不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id, is_deleted=False)
        except Product.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        # 检查商品是否可以创建交易
        # 商品不能是待审核、已售出、已下架、锁定中的状态
        if product.status not in ['available']:
            return Response({
                'code': 400,
                'message': '该商品当前不可购买'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 检查是否有其他有效的待付款交易
        existing_transaction = Transaction.objects.filter(
            product=product,
            status='pending',
            locked_until__gt=datetime.now()
        ).first()

        if existing_transaction:
            if existing_transaction.buyer == request.user:
                return Response({
                    'code': 400,
                    'message': '您已有一个有效的购买意向，请完成付款或等待过期'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'code': 400,
                    'message': '该商品已被其他用户锁定，请稍后再试'
                }, status=status.HTTP_400_BAD_REQUEST)

        # 不能购买自己的商品
        if product.seller == request.user:
            return Response({
                'code': 400,
                'message': '不能购买自己发布的商品'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 创建交易
        transaction = Transaction.objects.create(
            product=product,
            buyer=request.user,
            seller=product.seller,
            status='pending'
        )

        # 更新商品状态为锁定
        product.status = 'locked'
        product.save(update_fields=['status', 'updated_at'])

        return Response({
            'code': 200,
            'message': '购买意向已创建，请在3小时内完成付款',
            'data': TransactionSerializer(transaction).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        """付款操作"""
        try:
            transaction = Transaction.objects.get(pk=pk, buyer=request.user)
        except Transaction.DoesNotExist:
            return Response({
                'code': 404,
                'message': '交易不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        if transaction.status != 'pending':
            return Response({
                'code': 400,
                'message': '当前状态不允许付款'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 检查是否过期
        if transaction.locked_until and transaction.locked_until < timezone.now():
            transaction.status = 'expired'
            transaction.save()
            transaction.product.status = 'available'
            transaction.product.save(update_fields=['status', 'updated_at'])
            return Response({
                'code': 400,
                'message': '购买意向已过期，请重新创建'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 执行付款
        transaction.status = 'paid'
        transaction.save()

        # 更新商品为已售出
        transaction.product.status = 'sold'
        transaction.product.save(update_fields=['status', 'updated_at'])

        return Response({
            'code': 200,
            'message': '付款成功，等待卖家发货',
            'data': TransactionSerializer(transaction).data
        })

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消交易"""
        try:
            transaction = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response({
                'code': 404,
                'message': '交易不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        # 检查权限：买家或卖家都可以取消
        if transaction.buyer != request.user and transaction.seller != request.user:
            return Response({
                'code': 403,
                'message': '无权取消此交易'
            }, status=status.HTTP_403_FORBIDDEN)

        if transaction.status not in ['pending', 'paid']:
            return Response({
                'code': 400,
                'message': '当前状态不允许取消'
            }, status=status.HTTP_400_BAD_REQUEST)

        transaction.status = 'cancelled'
        transaction.save()

        # 如果商品是锁定状态，恢复为在售
        if transaction.product.status == 'locked':
            transaction.product.status = 'available'
        elif transaction.product.status == 'sold':
            transaction.product.status = 'available'
        transaction.product.save(update_fields=['status', 'updated_at'])

        return Response({
            'code': 200,
            'message': '交易已取消',
            'data': TransactionSerializer(transaction).data
        })

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """退款操作（买家申请退款）"""
        try:
            transaction = Transaction.objects.get(pk=pk, buyer=request.user)
        except Transaction.DoesNotExist:
            return Response({
                'code': 404,
                'message': '交易不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        # 只有已付款状态才能申请退款
        if transaction.status != 'paid':
            return Response({
                'code': 400,
                'message': '当前状态不允许退款'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 更新交易状态为已取消
        transaction.status = 'cancelled'
        transaction.save()

        # 恢复商品为在售状态
        transaction.product.status = 'available'
        transaction.product.save(update_fields=['status', 'updated_at'])

        return Response({
            'code': 200,
            'message': '退款申请已提交，订单已取消',
            'data': TransactionSerializer(transaction).data
        })

    @action(detail=True, methods=['post'])
    def ship(self, request, pk=None):
        """卖家发货"""
        try:
            transaction = Transaction.objects.get(pk=pk, seller=request.user)
        except Transaction.DoesNotExist:
            return Response({
                'code': 404,
                'message': '交易不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        if transaction.status != 'paid':
            return Response({
                'code': 400,
                'message': '当前状态不允许发货'
            }, status=status.HTTP_400_BAD_REQUEST)

        transaction.status = 'shipped'
        transaction.save()

        return Response({
            'code': 200,
            'message': '发货成功，等待买家确认收货',
            'data': TransactionSerializer(transaction).data
        })

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """买家确认收货，交易完成"""
        try:
            transaction = Transaction.objects.get(pk=pk, buyer=request.user)
        except Transaction.DoesNotExist:
            return Response({
                'code': 404,
                'message': '交易不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        if transaction.status != 'shipped':
            return Response({
                'code': 400,
                'message': '当前状态不允许确认收货'
            }, status=status.HTTP_400_BAD_REQUEST)

        transaction.status = 'completed'
        transaction.save()

        return Response({
            'code': 200,
            'message': '交易完成，感谢您的使用',
            'data': TransactionSerializer(transaction).data
        })
