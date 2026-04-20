from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer

User = get_user_model()


class RegisterView(APIView):
    """用户注册视图"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            # 再次检查学号是否已存在，避免唯一性约束错误
            student_id = request.data.get('student_id')
            if User.objects.filter(student_id=student_id).exists():
                return Response({
                    'code': 400,
                    'message': '注册失败: 该学号已被注册',
                    'errors': {'student_id': ['该学号已被注册']}
                }, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()
            return Response({
                'code': 200,
                'message': '注册成功',
                'data': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        # 构建详细的错误信息
        error_messages = []
        for field, errors in serializer.errors.items():
            for error in errors:
                if field == 'student_id':
                    error_messages.append(f'学号: {error}')
                elif field == 'name':
                    error_messages.append(f'姓名: {error}')
                elif field == 'password':
                    error_messages.append(f'密码: {error}')
                elif field == 'password2':
                    error_messages.append(f'确认密码: {error}')
                else:
                    error_messages.append(f'{field}: {error}')
        error_message = '注册失败: ' + '; '.join(error_messages)
        return Response({
            'code': 400,
            'message': error_message,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """用户登录视图"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            student_id = serializer.validated_data.get('student_id')
            password = serializer.validated_data.get('password')
            try:
                user = User.objects.get(student_id=student_id)
            except User.DoesNotExist:
                return Response({
                    'code': 401,
                    'message': '学号或密码错误'
                }, status=status.HTTP_401_UNAUTHORIZED)
            if not user.check_password(password):
                return Response({
                    'code': 401,
                    'message': '学号或密码错误'
                }, status=status.HTTP_401_UNAUTHORIZED)
            refresh = RefreshToken.for_user(user)
            return Response({
                'code': 200,
                'message': '登录成功',
                'data': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserSerializer(user).data
                }
            })
        return Response({
            'code': 400,
            'message': '登录失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """用户个人资料视图"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': UserSerializer(user).data
        })

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 200,
                'message': '更新成功',
                'data': serializer.data
            })
        return Response({
            'code': 400,
            'message': '更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
