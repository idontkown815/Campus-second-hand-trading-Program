from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminAllowInactiveJWTAuthentication(JWTAuthentication):
    """
    自定义JWT认证后端，允许超级管理员即使is_active为false也能登录
    """
    
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
        except KeyError:
            raise AuthenticationFailed('Token contained no recognizable user identification')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        
        # 对于超级管理员，跳过is_active检查
        if not user.is_active and not user.is_superuser:
            raise AuthenticationFailed('User is inactive')

        return user
