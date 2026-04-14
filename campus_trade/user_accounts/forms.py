from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .models import User

class UserRegisterForm(UserCreationForm):
    """用户注册表单"""
    name = forms.CharField(
        label="姓名",
        max_length=50,
    )
    student_id = forms.CharField(
        label="学号",
        max_length=8,
        min_length=8,
        help_text="学号必须为8位数",
    )
    grade = forms.CharField(
        label="年级",
        max_length=20,
    )
    major = forms.CharField(
        label="专业",
        max_length=100,
    )
    password1 = forms.CharField(
        label="密码",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="密码长度至少8位，包含字母和数字",
    )
    password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="请再次输入密码进行确认",
    )
    
    class Meta:
        model = User
        fields = ['name', 'student_id', 'grade', 'major', 'password1', 'password2']
        labels = {
        }
    
    def clean_password2(self):
        """验证密码一致性"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次输入的密码不一致")
        return password2
    
    def clean_student_id(self):
        """验证学号格式和唯一性"""
        student_id = self.cleaned_data.get('student_id')
        if not student_id.isdigit():
            raise forms.ValidationError("学号必须为数字")
        if len(student_id) != 8:
            raise forms.ValidationError("学号必须为8位数")
        # 检查学号是否已存在
        if User.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("该学号已被注册")
        return student_id
