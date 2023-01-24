from rest_framework import serializers
from .models import Task,Article,Record,Project
from ..rbac.serializers.user_serializer import UserListSerializer
from common.custom_exception import CustomException

class TaskSerializer(serializers.ModelSerializer):
    '''
    任务的序列化
    '''

    class Meta:
        model = Task
        fields="__all__"


class ArticleSerializer(serializers.ModelSerializer):
    '''
    文章的序列化
    '''
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Article
        fields="__all__"


class RecordSerializer(serializers.ModelSerializer):
    '''
    记录的序列化
    '''
    user = serializers.CharField(source="user.name")
    project = serializers.CharField(source="project.name")
    task = serializers.CharField(source="task.name")

    class Meta:
        model = Record
        fields="__all__"

class ProjectSerializer(serializers.ModelSerializer):
    '''
    项目的序列化
    '''
    members = UserListSerializer(many=True,read_only=True)

    class Meta:
        model = Project
        fields="__all__"