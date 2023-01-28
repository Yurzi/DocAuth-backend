from rest_framework import serializers
from .models import Task,Article,Record,Project,Task_User
from ..rbac.serializers.user_serializer import UserListSerializer
from common.custom_exception import CustomException



class TaskSerializer(serializers.ModelSerializer):
    '''
    任务的序列化
    '''

    def to_representation(self, instance):
        representation = super(TaskSerializer, self).to_representation(instance)
        representation['members'] = []
        for i in UserListSerializer(instance.members, many=True).data:
            reason = TaskUserSerializer(instance.task_user_set.get(task=instance.id, user=i['id'])).data['duty']
            i['duty'] = reason
            representation['members'].append(i)
        return representation

    class Meta:
        model = Task
        fields = '__all__'

class TaskUserSerializer(serializers.ModelSerializer):
    '''
    任务成员的序列化
    '''
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Task_User
        fields = '__all__'
        
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