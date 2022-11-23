from django.db import models
from apps.rbac.models import User
# Create your models here.

class Project(models.Model):
    STATUS_CHOICES = (
        ('s', 'Stop'),
        ('r', 'Running'),
    )
    name = models.CharField(max_length=30, verbose_name="项目名")
    desc = models.CharField(max_length=100, verbose_name="项目描述")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    status = models.CharField(verbose_name='Status (*)', max_length=1, choices=STATUS_CHOICES, default='r', null=False, blank=False)

    class Meta:
        verbose_name = "项目信息"
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = (
        ('s', 'Stop'),
        ('r', 'Running'),
    )
    name = models.CharField(max_length=30, verbose_name="任务名")
    desc = models.CharField(max_length=100, verbose_name="任务描述")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    status = models.CharField(verbose_name='Status (*)', max_length=1, choices=STATUS_CHOICES, default='r', null=False, blank=False)
    step = models.IntegerField(verbose_name="步骤", null=True, blank=True)
    type = models.CharField(max_length=30, verbose_name="类型", null=True, blank=True)
    number = models.IntegerField(verbose_name="编号", null=True, blank=True)

    class Meta:
        verbose_name = "任务信息"
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

class Article(models.Model):
    name = models.CharField(max_length=30, verbose_name="文章名")
    content = models.TextField(max_length=50000, verbose_name="文章内容")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    taskId = models.ForeignKey(Task, verbose_name="任务", on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "文章信息"
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Record(models.Model):
    TYPE_CHOICES = (

    )
    name = models.CharField(max_length=30, verbose_name="记录名")
    content = models.TextField(max_length=5000, verbose_name="记录内容")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    taskId = models.ForeignKey(Task, verbose_name="任务", on_delete=models.CASCADE, null=False, blank=False)
    projectId = models.ForeignKey(Project, verbose_name="项目", on_delete=models.CASCADE, null=False, blank=False)
    type = models.CharField(verbose_name='Type (*)', max_length=1, choices=TYPE_CHOICES, default='', null=False, blank=False)

    class Meta:
        verbose_name = "记录信息"
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

class Project_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="项目")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = "用户项目关系"
        verbose_name_plural = verbose_name
        ordering = ['user']

    def __str__(self):
        return self.user.name + " with " + self.project.name

class Task_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    project = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="任务")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = "用户任务关系"
        verbose_name_plural = verbose_name
        ordering = ['user']

    def __str__(self):
        return self.user.name + " with " + self.project.name