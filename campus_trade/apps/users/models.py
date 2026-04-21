from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户模型"""
    name = models.CharField(max_length=50, verbose_name="姓名", null=False, blank=False, default="")
    student_id = models.CharField(max_length=8, unique=True, verbose_name="学号", error_messages={
        'unique': '该学号已被注册'
    })
    grade = models.CharField(max_length=20, verbose_name="年级", null=True, blank=True)
    major = models.CharField(max_length=50, verbose_name="专业", null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="头像")
    
    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'
