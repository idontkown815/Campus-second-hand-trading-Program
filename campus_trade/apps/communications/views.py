from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, Favorite, Report, Block
from .serializers import ConversationSerializer, MessageSerializer, FavoriteSerializer, ReportSerializer, BlockSerializer


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
