from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

User = get_user_model()

def validate_password(value):
    """验证密码是否包含数字和字母或字符"""
    if len(value) < 8:
        raise serializers.ValidationError("密码长度至少8位")
    # 检查是否包含数字
    if not re.search(r'\d', value):
        raise serializers.ValidationError("密码应包含数字和字母或字符")
    # 检查是否包含字母或特殊字符
    if not re.search(r'[a-zA-Z!@#$%^&*(),.?":{}|<>]', value):
        raise serializers.ValidationError("密码应包含数字和字母或字符")
    return value


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['student_id', 'password', 'password2', 'name', 'grade', 'major']
        extra_kwargs = {
            'name': {'required': False},
            'grade': {'required': False},
            'major': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "两次输入的密码不一致"})
        return attrs

    def validate_student_id(self, value):
        if not value.isdigit() or len(value) != 8:
            raise serializers.ValidationError("学号必须为8位数字")
        # 检查学号是否已被注册
        if User.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("该学号已被注册")
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        # 确保提供username参数，因为create_user()方法需要它
        username = validated_data.get('student_id')
        user = User.objects.create_user(username=username, **validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    student_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""
    class Meta:
        model = User
        fields = ['id', 'name', 'student_id', 'grade', 'major', 'avatar']
