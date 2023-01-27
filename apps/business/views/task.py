from rest_framework import status, request
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView
from common.custom_response import CustomResponse
from common.custom_exception import CustomException
from ..serializers import TaskSerializer,RecordSerializer
from ..models import Task,Record,Article
import uuid

def getSearchObject(query,queries:list[str]):
  res = {}
  for key in queries:
    if key in query:
      res[key] = query[key]
  return res

class TaskView(APIView):

  def get(self, request:request.Request, pk, format=None):
    '''获取任务列表'''
    searchObj = getSearchObject(request.query_params,['user','project'])
    tasks = Task.objects.all()
    if 'user' in searchObj:
      tasks = tasks.filter(members__id=searchObj['user'])
    if 'project' in searchObj:
      tasks = tasks.filter(project=searchObj['project'])
    serializer = TaskSerializer(tasks, many=True)
    return CustomResponse(data=serializer.data, status=status.HTTP_200_OK, message="获取任务列表成功")

  def put(self, request, pk, format=None):
    '''修改任务'''
    task = Task.objects.get(pk=request.data["task"])
    if(task is None):
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
      searchObj = getSearchObject(self.request.query_params,['user','project','task'])
      queryset = self.queryset.filter(**searchObj)
      return queryset

class SubmitTaskView(CreateAPIView):
  def post(self, request, pk, format=None):
    '''提交任务某一个步骤'''
    task = Task.objects.get(pk=request.data["task"])
    if(task is None):
      raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message="任务不存在")
    if(task.status == 'f' or task.step >= 5):
      raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message="任务已经完成")
    step = task.step
    Record.objects.filter(task=task, type=step).update(status='s')
    Record.objects.create(task=task, user=request.user, content=request.data["content"],type=step,name=uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org'),status='r')

    task.step = task.step + 1
    task.save(force_update=True)
    return CustomResponse(status=status.HTTP_200_OK, message="修改任务成功")


class FinishTaskView(CreateAPIView):
  def post(self, request, pk, format=None):
    '''完成任务'''
    task = Task.objects.get(pk=request.data["task"])
    if(task is None):
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
