from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(
        max_length=30, default="unknown", verbose_name="姓名")
    username = models.CharField(max_length=30, verbose_name="账号")
    phone = models.CharField(max_length=20, verbose_name="电话")
    password = models.CharField(max_length=100, verbose_name="密码")
    addTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name + " with " + self.username
