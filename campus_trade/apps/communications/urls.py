from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet, FavoriteViewSet, ReportViewSet, BlockViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'blocks', BlockViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
