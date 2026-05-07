from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, Favorite, Report, Block, Comment
from .serializers import ConversationSerializer, MessageSerializer, FavoriteSerializer, ReportSerializer, BlockSerializer, CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """评论视图"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # 获取评论列表不需要登录
        if self.action == 'list':
            return []
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        # 获取商品ID
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({
                'code': 400,
                'message': '请提供商品ID',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        # 只返回该商品的评论
        queryset = Comment.objects.filter(product_id=product_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        # 创建评论
        data = request.data.copy()
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            # 保存时传入当前用户
            serializer.save(user=request.user)
            return Response({
                'code': 200,
                'message': '评论成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': 400,
            'message': '评论失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        # 删除评论
        try:
            comment = self.get_object()

            # 权限检查：评论发布者或商品发布者可以删除
            is_comment_owner = comment.user == request.user
            is_product_owner = comment.product.seller == request.user

            if not (is_comment_owner or is_product_owner):
                return Response({
                    'code': 403,
                    'message': '无权删除此评论',
                    'data': None
                }, status=status.HTTP_403_FORBIDDEN)

            comment.delete()
            return Response({
                'code': 200,
                'message': '删除成功',
                'data': None
            })
        except Comment.DoesNotExist:
            return Response({
                'code': 404,
                'message': '评论不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)


class ConversationViewSet(viewsets.ModelViewSet):
    """会话视图"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # 只返回当前用户参与的会话
        queryset = Conversation.objects.filter(participants=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })


class MessageViewSet(viewsets.ModelViewSet):
    """消息视图"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # 只返回当前用户参与的会话的消息
        conversation_id = request.query_params.get('conversation_id')
        if conversation_id:
            queryset = Message.objects.filter(
                conversation_id=conversation_id,
                conversation__participants=request.user
            )
            # 标记消息为已读
            queryset.filter(sender__ne=request.user).update(is_read=True)
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })
        return Response({
            'code': 400,
            'message': '请提供会话ID'
        }, status=status.HTTP_400_BAD_REQUEST)


class FavoriteViewSet(viewsets.ModelViewSet):
    """收藏视图"""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # 只返回当前用户的收藏
        queryset = Favorite.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })


class ReportViewSet(viewsets.ModelViewSet):
    """举报视图"""
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]


class BlockViewSet(viewsets.ModelViewSet):
    """拉黑视图"""
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # 只返回当前用户的拉黑列表
        queryset = Block.objects.filter(blocker=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })
