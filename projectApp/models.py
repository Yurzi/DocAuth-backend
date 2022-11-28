from django.db import models


# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    passWord = models.CharField(max_length=64)
    age = models.IntegerField(default=2)
    username = models.CharField(max_length=32)
    addTime = models.DateTimeField()


class Project(models.Model):
    name = models.CharField(max_length=32)
    status = models.IntegerField(default=0)
    addTime = models.DateTimeField()


class Project_User(models.Model):
    project = models.ForeignKey(to="Project", on_delete=models.CASCADE)
    userId = models.ForeignKey(to="UserInfo", on_delete=models.CASCADE)
    addTime = models.DateTimeField()


class Project_UserRelation(models.Model):
    projectId = models.ForeignKey(to="Project", on_delete=models.CASCADE)
    userId = models.ForeignKey(to="UserInfo", on_delete=models.CASCADE)
    addTime = models.DateTimeField()


class Task(models.Model):
    projectId = models.IntegerField()
    number = models.IntegerField()
    name = models.CharField(max_length=32)
    step = models.IntegerField(default=0)
    type = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    addTime = models.DateTimeField()


class Task_User(models.Model):
    taskId = models.ForeignKey(to="Task", on_delete=models.CASCADE)
    userId = models.ForeignKey(to="UserInfo", on_delete=models.CASCADE)
    step = models.IntegerField()
    addTime = models.DateTimeField()

# class procedure(models.Model):
#     name = models.CharField(max_length=32)
