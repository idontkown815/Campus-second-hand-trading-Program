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
        return Product.objects.filter(is_deleted=False).exclude(status='rejected')

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
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 200,
                'message': '发布成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
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
        
        # 确保上传目录存在
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # 保存文件
        filename = fs.save(os.path.join('uploads', file.name), file)
        url = fs.url(filename)
        
        return Response({
            'code': 200,
            'message': '上传成功',
            'data': {'url': url}
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
