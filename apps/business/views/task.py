from rest_framework import status, request
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView
from common.custom_response import CustomResponse
from common.custom_exception import CustomException
from ..serializers import TaskSerializer,RecordSerializer,TaskUserSerializer
from ..models import Task,Record,Article,Task_User
from ...rbac.models import User
import uuid

def getSearchObject(query,queries:list[str]):
  res = {}
  for key in queries:
    if key in query and (query[key] != '' or query[key] != -1):
      res[key] = query[key]
  return res

class Task_UserListViews(ListAPIView):
    queryset = Task_User.objects.all()
    serializer_class = TaskUserSerializer

    def get_queryset(self):
      searchObj = getSearchObject(self.request.query_params,['user','duty','task'])
      queryset = self.queryset.filter(**searchObj)
      return queryset

class TaskView(APIView):
  def get(self, request:request.Request, pk, format=None):
    '''获取某个task'''
    try:
      task = Task.objects.get(pk=pk)
    except:
      raise CustomException(status_code=status.HTTP_404_NOT_FOUND,code=404, message="任务不存在")
    serializer = TaskSerializer(task)
    return CustomResponse(data=serializer.data, status=status.HTTP_200_OK, message="获取任务成功")

  def put(self, request, pk, format=None):
    '''修改任务'''
    try:
      task = Task.objects.get(pk=pk)
    except:
      raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message="任务不存在")
    serializer = TaskSerializer(task, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return CustomResponse(data=serializer.data, status=status.HTTP_200_OK, message="修改任务成功")


class RecordListView(ListAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    ordering_fields = ('status',)

    def get_queryset(self):
      searchObj = getSearchObject(self.request.query_params,['user','project','task','type','status'])
      queryset = self.queryset.filter(**searchObj)
      return queryset

class SubmitTaskView(CreateAPIView):
  def post(self, request, pk, format=None):
    '''提交任务某一个步骤'''
    try:
      task = Task.objects.get(pk=pk)
    except:
      raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message="任务不存在")
    if(task.status == 'f' or task.step >= 5):
      raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message="任务已经完成")
    step = task.step
    Record.objects.filter(task=task, type=step,status='r').update(status='s')
    if not 'content' in request.data:
      raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message="内容不能为空")
    
    try:
      user = User.objects.get(pk=request.data["user"])
    except:
      raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message="用户不存在")

    Record.objects.create(task=task, user=user, content=request.data["content"],type=step,name=str(uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org'))[-20:],status='r',project=task.project)

    task.step = task.step + 1
    task.save(force_update=True)
    return CustomResponse(status=status.HTTP_200_OK, message="提交成功")


class FinishTaskView(CreateAPIView):
  def post(self, request, pk, format=None):
    '''完成任务'''
    try:
      task = Task.objects.get(pk=request.data["task"])
    except:
      raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message="任务不存在")

    Record.objects.filter(task=task, status='r').update(status='f')
    task.status = 'f'
    task.step = 5
    task.save(force_update=True)

    records = Record.objects.filter(task=task, status='f')
    contents = ''
    for r in records:
      contents = contents + r.content
    Article.objects.create(task=task, content=contents)
    return CustomResponse(status=status.HTTP_200_OK, message="修改任务成功")
