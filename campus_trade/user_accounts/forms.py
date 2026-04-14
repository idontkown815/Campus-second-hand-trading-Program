from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .models import User

class UserRegisterForm(UserCreationForm):
    """用户注册表单"""
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
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': '用户名',
        }
        help_texts = {
            'username': None,
        }
    
    def clean_password2(self):
        """验证密码一致性"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次输入的密码不一致")
        return password2
