from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import createMD5
# Create your models here.

# 代替了系统自带的权限管理的用户表


class User(AbstractUser):
    name = models.CharField(max_length=30, default="unknown", verbose_name="姓名")
    username = models.CharField(max_length=30, verbose_name="账号", unique=True)
    phone = models.CharField(max_length=20, verbose_name="电话")
    password = models.CharField(max_length=100, verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱",max_length=100, null=True, blank=True)
    REQUIRED_FIELDS: list[str] = [ 'phone', 'password']
    USERNAME_FIELD = "username"


    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['username']

    def __str__(self):
        return self.name + " with " + self.username
    


class Role(models.Model):
    STATUS_CHOICES = (
        ('s', '停止使用'),
        ('r', '正在使用'),
    )
    name = models.CharField(max_length=30, verbose_name="角色名")
    desc = models.CharField(max_length=100, verbose_name="角色描述",blank=True)
    status = models.CharField(verbose_name='Status (*)', max_length=1, choices=STATUS_CHOICES, default='r', null=False, blank=False)
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    REQUIRED_FIELDS: list[str] = [ 'name']

    class Meta:
        verbose_name = "角色信息"
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name



class Api(models.Model):
    STATUS_CHOICES = (
        ('s', '停止使用'),
        ('r', '正在使用'),
        ('d', '开发中'),
    )
    name = models.CharField(max_length=30, verbose_name="接口名")
    path = models.CharField(max_length=30, verbose_name="接口路径")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    status = models.CharField(verbose_name='Status (*)', max_length=1, choices=STATUS_CHOICES, default='r', null=False, blank=False)
    REQUIRED_FIELDS: list[str] = [ 'name','path']


    class Meta:
        verbose_name = "接口信息"
        verbose_name_plural = verbose_name
        ordering = ['path']

    def __str__(self):
        return self.name + " : " + self.path

class Page(models.Model):
    STATUS_CHOICES = (
        ('s', '停止使用'),
        ('r', '正在使用'),
        ('d', '开发中'),
    )
    TYPE_CHOICES = (
        (),
        ()
    )
    name = models.CharField(max_length=30, verbose_name="页面名")
    path = models.CharField(max_length=30, verbose_name="页面路径")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    status = models.CharField(verbose_name='Status (*)', max_length=1, choices=STATUS_CHOICES, default='r', null=False, blank=False)
    parent = models.IntegerField(verbose_name="父页面ID", null=True, blank=True)
    REQUIRED_FIELDS: list[str] = [ 'name','path']


    class Meta:
        verbose_name = "页面信息"
        verbose_name_plural = verbose_name
        ordering = ['path']

    def __str__(self):
        return self.name + " : " + self.path

class Function(models.Model):
    STATUS_CHOICES = (
        ('s', '停止使用'),
        ('r', '正在使用'),
        ('d', '开发中'),
    )
    name = models.CharField(max_length=100, verbose_name="功能名")
    key = models.CharField(max_length=30, verbose_name="功能函数名")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    status = models.CharField(verbose_name='Status (*)', max_length=1, choices=STATUS_CHOICES, default='r', null=False, blank=False)
    REQUIRED_FIELDS: list[str] = [ 'name','key']


    class Meta:
        verbose_name = "功能信息"
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

class Role_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="角色")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = "用户角色关系"
        verbose_name_plural = verbose_name
        ordering = ['user']

    def __str__(self):
        return self.user.name + " with " + self.role.name

class Role_Page(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="角色")
    page = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name="页面")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = "角色页面关系"
        verbose_name_plural = verbose_name
        ordering = ['role']

    def __str__(self):
        return self.role.name + " with " + self.page.name

class API_Page(models.Model):
    api = models.ForeignKey(Api, on_delete=models.CASCADE, verbose_name="接口")
    page = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name="页面")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = "接口页面关系"
        verbose_name_plural = verbose_name
        ordering = ['api']

    def __str__(self):
        return self.api.name + " with " + self.page.name



class Role_Function(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="角色")
    function = models.ForeignKey(Function, on_delete=models.CASCADE, verbose_name="功能")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = "角色功能关系"
        verbose_name_plural = verbose_name
        ordering = ['role']

    def __str__(self):
        return self.role.name + " with " + self.function.name

class Api_Function(models.Model):
    api = models.ForeignKey(Api, on_delete=models.CASCADE, verbose_name="接口")
    function = models.ForeignKey(Function, on_delete=models.CASCADE, verbose_name="功能")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = "接口功能关系"
        verbose_name_plural = verbose_name
        ordering = ['api']

    def __str__(self):
        return self.api.name + " with " + self.function.name

