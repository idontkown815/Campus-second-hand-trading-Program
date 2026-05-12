from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


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
        serializer = self.get_serializer(queryset, many=True)
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
        
        serializer = self.get_serializer(instance)
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
            # 检查是否是商品的发布者
            if product.seller != request.user:
                return Response({
                    'code': 403,
                    'message': '无权操作此商品',
                    'data': None
                }, status=status.HTTP_403_FORBIDDEN)
            
            # 检查商品状态是否允许修改
            if product.status not in ['pending', 'available']:
                return Response({
                    'code': 400,
                    'message': '只有待审核或在售的商品可以修改',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 执行更新操作
            serializer = self.get_serializer(product, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
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
        fs = FileSystemStorage()
        
        # 保存文件（直接保存到uploads目录）
        filename = fs.save(file.name, file)
        
        # 只返回文件名，而不是完整URL
        # 这样存储到数据库的是相对路径，序列化器会根据当前环境构建完整URL
        return Response({
            'code': 200,
            'message': '上传成功',
            'data': {'url': filename}
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def take_down(self, request, pk=None):
        try:
            product = self.get_object()
            # 检查是否是商品的发布者
            if product.seller != request.user:
                return Response({
                    'code': 403,
                    'message': '无权操作此商品',
                    'data': None
                }, status=status.HTTP_403_FORBIDDEN)
            
            # 将商品状态改为已下架
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
    def put_on_shelf(self, request, pk=None):
        """上架商品"""
        try:
            product = self.get_object()
            # 检查是否是商品的发布者
            if product.seller != request.user:
                return Response({
                    'code': 403,
                    'message': '无权操作此商品',
                    'data': None
                }, status=status.HTTP_403_FORBIDDEN)
            
            # 检查商品状态是否允许上架（允许待审核、已下架、锁定中的商品上架）
            if product.status not in ['pending', 'rejected', 'locked']:
                return Response({
                    'code': 400,
                    'message': '只有待审核、已下架或锁定中的商品可以上架',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 将商品状态改为在售
            product.status = 'available'
            product.save()
            
            return Response({
                'code': 200,
                'message': '商品已上架',
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
        # 获取当前用户发布的商品
        products = Product.objects.filter(seller=request.user, is_deleted=False)
        serializer = self.get_serializer(products, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })
