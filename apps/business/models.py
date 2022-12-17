from django.db import models
from apps.rbac.models import User


# Create your models here.

class Project(models.Model):
    STATUS_CHOICES = (
        ('s', '暂停中'),
        ('r', '进行中'),
        ('f', '已完成'),
    )
    name = models.CharField(max_length=30, verbose_name="项目名")
    desc = models.CharField(max_length=100, verbose_name="项目描述", blank=True, null=True)
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    status = models.CharField(verbose_name='Status (*)', max_length=1, choices=STATUS_CHOICES, default='r', null=False,
                              blank=False)
    members = models.ManyToManyField(User, verbose_name='项目成员', through='Project_User')
    REQUIRED_FIELDS: list[str] = ['name']

    class Meta:
        verbose_name = "项目信息"
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = (
        ('s', '暂停中'),
        ('r', '进行中'),
        ('f', '已完成'),
    )
    STEP_CHOICES = (
        (1, '编撰中'),
        (2, '审阅中'),
        (3, '批阅中'),
        (4, '汇签中'),
    )
    TYPE_CHOICES = (
        (1, '一般项目任务'),
        (2, '系统生成任务'),
    )
    name = models.CharField(max_length=30, verbose_name="任务名")
    desc = models.CharField(max_length=100, verbose_name="任务描述", default="")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    startTime = models.DateTimeField(verbose_name='任务预定开始时间')
    deadLine = models.DateTimeField(verbose_name="任务预定截止时间")
    status = models.CharField(verbose_name='Status (*)', max_length=1, choices=STATUS_CHOICES, default='r')
    step = models.IntegerField(verbose_name="当前步骤", choices=STEP_CHOICES, default=1)
    type = models.IntegerField(verbose_name="类型", choices=TYPE_CHOICES)
    thisId = models.IntegerField(verbose_name="在某一阶段中此任务的相对id", default=0)
    thisFarther = models.IntegerField(verbose_name="在某一阶段中此任务的父结点id", default=0)
    phase = models.IntegerField(verbose_name="任务阶段", default=0)
    REQUIRED_FIELDS: list[str] = ['name', 'type']

    class Meta:
        verbose_name = "任务信息"
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    task = models.ForeignKey(Task, verbose_name="任务", on_delete=models.CASCADE, null=False, blank=False)
    content = models.TextField(max_length=50000, verbose_name="文章内容", default="")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = "文章信息"
        verbose_name_plural = verbose_name
        ordering = ['task']

    def __str__(self):
        return str(self.task) + "的文章"


class Record(models.Model):
    TYPE_CHOICES = (
        (1, '编撰'),
        (2, '审阅'),
        (3, '批阅'),
        (4, '汇签'),
        (5, '打回'),
    )
    project = models.ForeignKey(Project, verbose_name="项目", on_delete=models.CASCADE, null=False, blank=False)
    task = models.ForeignKey(Task, verbose_name="任务", on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, verbose_name="执行者", on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=30, verbose_name="记录名")
    type = models.IntegerField(verbose_name='Type (*)', choices=TYPE_CHOICES)
    content = models.TextField(max_length=5000, verbose_name="记录内容")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    REQUIRED_FIELDS: list[str] = ['name', 'type']

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


class Task_Project(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="任务")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="项目")
    number = models.IntegerField(verbose_name="是项目的第几个任务")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    REQUIRED_FIELDS: list[str] = ['number']

    class Meta:
        verbose_name = "项目任务关系"
        verbose_name_plural = verbose_name
        ordering = ['project']

    def __str__(self):
        return self.project.name + " with " + self.task.name


class Task_User(models.Model):
    TYPE_CHOICES = (
        (1, '编撰'),
        (2, '审阅'),
        (3, '批阅'),
        (4, '汇签1'),
        (5, '汇签2'),
        (6, '打回'),
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="任务")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    addTime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    type = models.IntegerField(verbose_name='Type (*)', choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "用户任务关系"
        verbose_name_plural = verbose_name
        ordering = ['user']

    def __str__(self):
        return self.user.name + " with " + self.task.name
