from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
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
        queryset = Conversation.objects.filter(participants=request.user)
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        print("=== 创建会话请求到达 ===")
        print(f"请求方法: {request.method}")
        print(f"请求数据: {request.data}")
        print(f"请求头: {dict(request.headers)}")
        
        data = request.data
        product_id = data.get('product_id')
        participant_ids = data.get('participant_ids', [])
        initial_message = data.get('initial_message', '')

        print(f"product_id: {product_id}, type: {type(product_id)}")
        print(f"participant_ids: {participant_ids}, type: {type(participant_ids)}")
        print(f"initial_message: {initial_message}")

        if not product_id:
            print("错误: 缺少商品ID")
            return Response({
                'code': 400,
                'message': '请提供商品ID',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_id = int(product_id)
        except (ValueError, TypeError):
            return Response({
                'code': 400,
                'message': '商品ID必须为整数',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        from apps.products.models import Product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        if not isinstance(participant_ids, list):
            participant_ids = []
        
        try:
            participant_ids = [int(pid) for pid in participant_ids]
        except (ValueError, TypeError):
            return Response({
                'code': 400,
                'message': '参与者ID必须为整数列表',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        all_participant_ids = list(set(participant_ids + [request.user.id]))

        try:
            existing_conversation = Conversation.objects.filter(
                product=product,
                participants=request.user
            ).first()

            if existing_conversation:
                serializer = self.get_serializer(existing_conversation, context={'request': request})
                return Response({
                    'code': 200,
                    'message': '会话已存在',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

            conversation = Conversation.objects.create(product=product)
            conversation.participants.set(all_participant_ids)

            if initial_message:
                Message.objects.create(
                    conversation=conversation,
                    sender=request.user,
                    content=initial_message
                )

            serializer = self.get_serializer(conversation, context={'request': request})
            return Response({
                'code': 201,
                'message': '创建成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'code': 500,
                'message': f'服务器错误: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MessageViewSet(viewsets.ModelViewSet):
    """消息视图"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        print("=== 获取消息请求到达 ===")
        print(f"请求用户: {request.user}")
        print(f"请求参数: {request.query_params}")
        
        # 只返回当前用户参与的会话的消息
        conversation_id = request.query_params.get('conversation_id')
        print(f"conversation_id: {conversation_id}, type: {type(conversation_id)}")
        
        if conversation_id:
            try:
                conversation_id = int(conversation_id)
                queryset = Message.objects.filter(
                    conversation_id=conversation_id,
                    conversation__participants=request.user
                )
                print(f"找到消息数量: {queryset.count()}")
                
                # 标记消息为已读
                Message.objects.filter(
                    conversation_id=conversation_id,
                    conversation__participants=request.user
                ).exclude(sender=request.user).update(is_read=True)
                
                serializer = self.get_serializer(queryset, many=True)
                print("返回成功")
                return Response({
                    'code': 200,
                    'message': '获取成功',
                    'data': serializer.data
                })
            except Exception as e:
                print(f"获取消息失败: {str(e)}")
                return Response({
                    'code': 500,
                    'message': f'获取消息失败: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            'code': 400,
            'message': '请提供会话ID'
        }, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        print("=== 发送消息请求到达 ===")
        print(f"请求用户: {request.user}")
        print(f"请求数据: {request.data}")
        
        conversation_id = request.data.get('conversation_id')
        content = request.data.get('content')
        
        print(f"conversation_id: {conversation_id}, content: {content}")
        
        if not conversation_id:
            return Response({
                'code': 400,
                'message': '请提供会话ID'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not content:
            return Response({
                'code': 400,
                'message': '请提供消息内容'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            conversation_id = int(conversation_id)
            conversation = Conversation.objects.get(id=conversation_id)
            
            # 检查用户是否是会话参与者
            if request.user not in conversation.participants.all():
                return Response({
                    'code': 403,
                    'message': '无权发送消息到该会话'
                }, status=status.HTTP_403_FORBIDDEN)
            
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            
            # 更新会话的最后消息
            conversation.last_message = message
            conversation.save()
            
            serializer = self.get_serializer(message)
            print("消息发送成功")
            return Response({
                'code': 200,
                'message': '发送成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except Conversation.DoesNotExist:
            print("会话不存在")
            return Response({
                'code': 404,
                'message': '会话不存在'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"发送消息失败: {str(e)}")
            return Response({
                'code': 500,
                'message': f'发送消息失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FavoriteViewSet(viewsets.ModelViewSet):
    """收藏视图"""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # 只返回当前用户的收藏
        queryset = Favorite.objects.filter(user=request.user).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        # 创建收藏
        product_id = request.data.get('product_id')
        
        if not product_id:
            return Response({
                'code': 400,
                'message': '请提供商品ID',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_id = int(product_id)
        except (ValueError, TypeError):
            return Response({
                'code': 400,
                'message': '商品ID必须为整数',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        from apps.products.models import Product
        try:
            product = Product.objects.get(id=product_id, is_deleted=False, status='available')
        except Product.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        # 检查是否已收藏
        existing_favorite = Favorite.objects.filter(user=request.user, product=product).first()
        if existing_favorite:
            return Response({
                'code': 400,
                'message': '您已收藏此商品',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        favorite = Favorite.objects.create(user=request.user, product=product)
        serializer = self.get_serializer(favorite, context={'request': request})
        return Response({
            'code': 200,
            'message': '收藏成功',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        # 删除收藏
        try:
            favorite = self.get_object()
            if favorite.user != request.user:
                return Response({
                    'code': 403,
                    'message': '无权取消此收藏',
                    'data': None
                }, status=status.HTTP_403_FORBIDDEN)
            
            favorite.delete()
            return Response({
                'code': 200,
                'message': '取消收藏成功',
                'data': None
            })
        except Favorite.DoesNotExist:
            return Response({
                'code': 404,
                'message': '收藏不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def check(self, request):
        """检查商品是否已收藏"""
        product_id = request.query_params.get('product_id')
        
        if not product_id:
            return Response({
                'code': 400,
                'message': '请提供商品ID',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_id = int(product_id)
        except (ValueError, TypeError):
            return Response({
                'code': 400,
                'message': '商品ID必须为整数',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        is_favorited = Favorite.objects.filter(user=request.user, product_id=product_id).exists()
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': {'is_favorited': is_favorited}
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
