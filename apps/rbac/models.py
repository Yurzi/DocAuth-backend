from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# 代替了系统自带的权限管理的用户表


class User(AbstractUser):
    name = models.CharField(
        max_length=30, default="unknown", verbose_name="姓名")
    username = models.CharField(max_length=30, verbose_name="账号", unique=True)
    phone = models.CharField(max_length=20, verbose_name="电话")
    password = models.CharField(max_length=100, verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱",max_length=100, null=True, blank=True)
    REQUIRED_FIELDS: list[str] = [ 'phone', 'password']

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['username']

    def __str__(self):
        return self.name + " with " + self.username
