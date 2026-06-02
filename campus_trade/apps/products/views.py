from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from apps.transactions.models import Transaction


class CategoryViewSet(viewsets.ModelViewSet):
    """分类视图"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })


class ProductViewSet(viewsets.ModelViewSet):
    """商品视图"""
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)

        # 商品大厅只显示在售且库存大于0的商品
        queryset = queryset.filter(status='available', stock__gt=0)

        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(description__icontains=search)

        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)

        min_price = self.request.query_params.get('min_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        max_price = self.request.query_params.get('max_price', None)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        campus = self.request.query_params.get('campus', None)
        if campus:
            queryset = queryset.filter(campus_location=campus)

        sort = self.request.query_params.get('sort', None)
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')

        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        # 对于商品详情，使用不过滤状态的查询
        queryset = Product.objects.filter(is_deleted=False)
        try:
            instance = queryset.get(pk=kwargs.get('pk'))
        except Product.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 允许卖家和买家访问商品详情
        is_buyer = request.user and instance.transactions.filter(buyer=request.user).exists()
        is_seller = request.user and instance.seller == request.user
        
        if not (is_buyer or is_seller) and instance.status != 'available':
            return Response({
                'code': 403,
                'message': '无权访问此商品',
                'data': None
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, context={'request': request})
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        import logging
        logger = logging.getLogger('django')
        logger.info(f"收到商品发布请求，用户: {request.user}, 数据: {request.data}")
        
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            logger.info("序列化器验证通过")
            serializer.save()
            return Response({
                'code': 200,
                'message': '发布成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        logger.error(f"序列化器验证失败，错误: {serializer.errors}")
        return Response({
            'code': 400,
            'message': '发布失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            product = self.get_object()
            if product.seller != request.user:
                return Response({
                    'code': 403,
                    'message': '无权操作此商品',
                    'data': None
                }, status=status.HTTP_403_FORBIDDEN)
            
            if product.status not in ['pending', 'available']:
                return Response({
                    'code': 400,
                    'message': '只有待审核或在售的商品可以修改',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            original_status = product.status
            
            serializer = self.get_serializer(product, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                if original_status == 'available':
                    product.status = 'pending'
                    product.save(update_fields=['status'])
                
                serializer.save()
                
                if original_status == 'available':
                    return Response({
                        'code': 200,
                        'message': '修改成功，商品需要重新审核后才能上架',
                        'data': serializer.data
                    })
                return Response({
                    'code': 200,
                    'message': '修改成功',
                    'data': serializer.data
                })
            return Response({
                'code': 400,
                'message': '修改失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def upload(self, request):
        if 'file' not in request.FILES:
            return Response({
                'code': 400,
                'message': '未上传文件',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        # 指定存储到 商品 子目录
        fs = FileSystemStorage(location=str(settings.MEDIA_ROOT / '商品'))
        
        # 保存文件（保存到uploads/商品目录）
        filename = fs.save(file.name, file)
        
        # 返回相对路径（包含商品/前缀），序列化器会根据当前环境构建完整URL
        return Response({
            'code': 200,
            'message': '上传成功',
            'data': {'url': '商品/' + filename}
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def take_down(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk, is_deleted=False)
            if product.seller != request.user:
                return Response({
                    'code': 403,
                    'message': '无权操作此商品',
                    'data': None
                }, status=status.HTTP_403_FORBIDDEN)
            
            product.status = 'rejected'
            product.save()
            
            return Response({
                'code': 200,
                'message': '商品已下架',
                'data': None
            })
        except Product.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def admin_take_down(self, request, pk=None):
        """管理员：强制下架商品"""
        if not request.user.is_superuser:
            return Response({
                'code': 403,
                'message': '只有管理员可以执行此操作',
                'data': None
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            product = Product.objects.get(pk=pk, is_deleted=False)
            product.status = 'violation'
            product.save()
            
            return Response({
                'code': 200,
                'message': '商品已下架',
                'data': None
            })
        except Product.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def put_on_shelf(self, request, pk=None):
        """上架商品"""
        try:
            product = Product.objects.get(pk=pk, is_deleted=False)
            if product.seller != request.user:
                return Response({
                    'code': 403,
                    'message': '无权操作此商品',
                    'data': None
                }, status=status.HTTP_403_FORBIDDEN)
            
            if product.status not in ['rejected', 'locked']:
                return Response({
                    'code': 400,
                    'message': '只有已下架或锁定中的商品可以上架',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            product.status = 'pending'
            product.save()
            
            return Response({
                'code': 200,
                'message': '商品已提交审核，请等待管理员审核通过后上架',
                'data': None
            })
        except Product.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_products(self, request):
        products = Product.objects.filter(seller=request.user, is_deleted=False)
        serializer = self.get_serializer(products, many=True, context={'request': request})
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def pending_list(self, request):
        """管理员：获取待审核商品列表"""
        if not request.user.is_superuser:
            return Response({
                'code': 403,
                'message': '只有管理员可以执行此操作',
                'data': None
            }, status=status.HTTP_403_FORBIDDEN)
        
        products = Product.objects.filter(status='pending', is_deleted=False)
        serializer = self.get_serializer(products, many=True, context={'request': request})
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        """管理员：审核通过商品"""
        if not request.user.is_superuser:
            return Response({
                'code': 403,
                'message': '只有管理员可以执行此操作',
                'data': None
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            product = Product.objects.get(pk=pk, is_deleted=False)
            if product.status != 'pending':
                return Response({
                    'code': 400,
                    'message': '只有待审核的商品可以通过',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            product.status = 'available'
            product.save()
            
            return Response({
                'code': 200,
                'message': '审核通过',
                'data': None
            })
        except Product.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        """管理员：审核拒绝商品"""
        if not request.user.is_superuser:
            return Response({
                'code': 403,
                'message': '只有管理员可以执行此操作',
                'data': None
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            product = Product.objects.get(pk=pk, is_deleted=False)
            if product.status != 'pending':
                return Response({
                    'code': 400,
                    'message': '只有待审核的商品可以拒绝',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            product.status = 'rejected'
            product.save()
            
            return Response({
                'code': 200,
                'message': '审核拒绝',
                'data': None
            })
        except Product.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def admin_products(self, request):
        """管理员：获取所有商品列表（包括待审核）"""
        if not request.user.is_superuser:
            return Response({
                'code': 403,
                'message': '只有管理员可以执行此操作',
                'data': None
            }, status=status.HTTP_403_FORBIDDEN)
        
        products = Product.objects.filter(is_deleted=False).order_by('-created_at')
        serializer = self.get_serializer(products, many=True, context={'request': request})
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def admin_stats(self, request):
        """管理员：获取统计数据"""
        if not request.user.is_superuser:
            return Response({
                'code': 403,
                'message': '只有管理员可以执行此操作',
                'data': None
            }, status=status.HTTP_403_FORBIDDEN)
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        total_users = User.objects.filter(is_active=True).count()
        total_products = Product.objects.filter(status='available', is_deleted=False).count()
        pending_products = Product.objects.filter(status='pending', is_deleted=False).count()
        
        from apps.transactions.models import Transaction
        total_transactions = Transaction.objects.count()
        
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {
                'totalUsers': total_users,
                'totalProducts': total_products,
                'pendingProducts': pending_products,
                'totalTransactions': total_transactions
            }
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def admin_release_all(self, request):
        """管理员：释放所有被锁定的商品"""
        # 检查是否是超级管理员
        if not request.user.is_superuser:
            return Response({
                'code': 403,
                'message': '只有管理员可以执行此操作',
                'data': None
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 统计
        locked_count = Product.objects.filter(status='locked').count()
        pending_count = Transaction.objects.filter(status='pending').count()
        
        # 更新
        product_updated = Product.objects.filter(status='locked').update(status='available')
        transaction_updated = Transaction.objects.filter(status='pending').update(status='expired')
        
        return Response({
            'code': 200,
            'message': '释放成功',
            'data': {
                'locked_released': product_updated,
                'pending_expired': transaction_updated
            }
        })
