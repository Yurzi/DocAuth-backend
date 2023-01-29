from rest_framework import status, request
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView
from common.custom_response import CustomResponse
from common.custom_exception import CustomException
from ..serializers import TaskSerializer,RecordSerializer,TaskUserSerializer
from ..models import Task,Record,Article,Task_User
from ...rbac.models import User
import uuid
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

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
    if(task.status == 'f'):
      raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message="任务已经完成")
    if(task.status == 'w'):
      raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message="任务待提交")
    if not 'content' in request.data or len(str(request.data["content"]).strip()) == 0:
      raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message="内容不能为空")
    try:
      user = User.objects.get(pk=request.data["user"])
    except:
      raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message="用户不存在")

    step = task.step
    Record.objects.filter(task=task, type=step,status='r').update(status='s')

    Record.objects.create(task=task, user=user, content=request.data["content"],type=step,name=str(uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org'))[-20:],status='r',project=task.project)

    if task.step <= 3:
      task.step = task.step + 1
    elif task.step == 4:
      task.status = 'w'
    task.save(force_update=True)
    return CustomResponse(status=status.HTTP_200_OK, message="提交成功")

class RevertTaskView(CreateAPIView):
  def post(self, request, pk, format=None):
    '''退回任务'''
    try:
      task = Task.objects.get(pk=pk)
    except:
      raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message="任务不存在")
    if(task.status == 'f'):
      raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message="任务已经完成")
    if not 'content' in request.data or len(str(request.data["content"]).strip()) == 0:
      raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message="内容不能为空")
    try:
      user = User.objects.get(pk=request.data["user"])
    except:
      raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message="用户不存在")

    Record.objects.filter(task=task, status='r').update(status='s')
    Record.objects.create(task=task, user=user, content=request.data["content"],type=5,name=str(uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org'))[-20:],status='f',project=task.project)
    task.step = 1
    task.status = 'r'
    task.save(force_update=True)
    return CustomResponse(status=status.HTTP_200_OK, message="退回成功")


def createTaskArticleContent(task:Task,records):
  contents = ''
  contents = contents +  '\n任务ID：' + str(task.pk)
  contents = contents +  '\n任务名称：' + str(task.name) 
  contents = contents +  '\n任务所属项目：' + str(task.project) 
  contents = contents +  '\n任务描述：' + str(task.desc)
  contents = contents +  '\n任务成员：' + str(task.members)
  contents = contents +  '\n任务创建时间：' + str(task.addTime)
  for r in records:
    recordCt = '\n\n' + '步骤：' + str(r.type) + '\n' + '提交人：' + str(r.user) + '\n' + '提交时间：' + str(r.addTime) + '\n' + '内容：' + str(r.content)
    contents = contents + recordCt
  return contents


class FinishTaskView(CreateAPIView):
  def post(self, request, pk, format=None):
    '''完成任务'''
    try:
      task = Task.objects.get(pk=pk)
    except:
      raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message="任务不存在")
    if task.status != 'w':
      raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message="任务状态不正确")

    Record.objects.filter(task=task, status='r').update(status='f')
    task.status = 'f'
    task.save(force_update=True)

    records = Record.objects.filter(task=task, status='f')
    
    contents = createTaskArticleContent(task,records)
    Article.objects.create(task=task, content=contents)

    return CustomResponse(status=status.HTTP_200_OK, message="完成任务成功")


class ArticlePDFView(RetrieveAPIView):
  def get(self, request, pk, format=None):
    '''获取任务PDF'''
    try:
      task= Task.objects.get(pk=pk)
    except:
      raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message="任务不存在")
    
    if task.status != 'f':
      raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message="任务未完成")

    try:
      article = Article.objects.get(task=task)
    except:
      raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message="文章不存在")

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, article.content)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=str(task) + '.pdf')