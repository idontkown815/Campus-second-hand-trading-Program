from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet

router = DefaultRouter()
router.register(r'', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/confirm/', TransactionViewSet.as_view({'put': 'confirm_transaction'}), name='confirm_transaction'),
]
