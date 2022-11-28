import datetime
from django.http.response import JsonResponse
from django.core import serializers
import json
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

from ..rbac.models import User
from .models import Project, Task, Task_User, Project_User
import datetime


# 向前端返回json数据
def respondDataToFront(preData):
    # data = serializers.serialize('json', preData)
    # jsondata = json.loads(data)
    data = {
        'code': 200,
        'message': "获取成功",
        'data': preData
    }
    print("完成发送任务")
    return JsonResponse(data=data, safe=False)


# 保存新建的项目
def saveProject(request):
    projectName = "项目1"
    Project.objects.create(name=projectName, status='r')
    return HttpResponse("成功")


# 根据用户id得到该用户所参加的所有项目列表
def getThisUserProjectList(request):
    thisUserId = request.GET.get("userId")
    print(thisUserId)
    projectList = Project_User.objects.filter(user=thisUserId).values_list("projectId__status",
                                                                                            "projectId__name",
                                                                                            "projectId__id",
                                                                                            "projectId__addTime"
                                                                                            ).distinct()
    print(projectList)
    # for obj in projectList:
    #     print(obj)
    # return HttpResponse(json.dumps(projectList))
    return respondDataToFront(list(projectList))


# 根据项目的pid得到该项目下的任务列表以及各任务对应的人员分配信息
def getTasksFromTheProject(request):
    projectName = "汽车电子系统制造工程"
    projectId = request.GET.get("projectId")
    print(projectId)
    TaskList = Task.objects.filter(project=projectId).values()
    userList = []
    applierList = []
    # 下面是默认两个阶段，每个阶段有若干个任务

    # print(list(models.Task_User.objects.filter(taskId=18).values("userId__username")))

    for task in TaskList:
        applierList.append(list(Task_User.objects.filter(task=task['id']).values("userId__username")))
    TaskList = list(TaskList)
    print(TaskList)
    for i in range(len(TaskList)):
        TaskList[i]['username'] = applierList[i]
    print(applierList)
    print(TaskList)
    return respondDataToFront(TaskList)


def saveTask(request):
    taskName = "阶段一任务一"
    taskType = 1  # 表示当前任务处于第几阶段
    dic = request.POST.get("userIdProcedureMap")
    print(dic[2])
    print(request.POST.get("taskName"))
    print("这里是用户列表")
    userIdProcedureMap = {2: 1, 3: 2, 4: 3, 1: 4}  # 前端传递的用户项目
    pId = 1  # 由前端将数据传递过来
    project = Project.objects.get(id=pId)
    # models.task.objects.create(name=projectName, status=0, addTime=datetime.datetime.now())

    # 1保存当前任务(互斥锁需要)
    Task.objects.create(project=pId, number=0, name=taskName,  type=taskType)
    task = Task.objects.last()

    # 2保存当前项目下的人员分工（互斥锁）
    for key in userIdProcedureMap.keys():
        userInfor = User.objects.get(id=key)
        Project_User.objects.create(project=project, user=userInfor)

    # 3保存当前任务下的人员分工(这个地方需要加锁)
    for key, value in userIdProcedureMap.items():
        userInfor = User.objects.get(id=key)
        Task_User.objects.create(task=task, user=userInfor, step=value)
    return HttpResponse("成功")


def test(request):
    projectId = 1
    m = list(Project.objects.all().values())
    data = {
        'data': m,
        'code': 200,
        'message': "获取成功"
    }
    print("完成发送任务")
    return JsonResponse(data=data, safe=False)
    # for obj in  lst:
    #     print(obj)

    # return HttpResponse("成功")


def orm(request):
    # models.UserInfo.objects.create(name= "ws1",passWord="123",age = 19)
    # models.UserInfo.objects.create(name= "ws2",passWord="123",age = 19)
    # models.UserInfo.objects.create(name= "ws3",passWord="123",age = 19)
    # models.UserInfo.objects.create(name= "ws4",passWord="123",age = 19)
    # 删除
    # models.UserInfo.objects.filter(id=1).delete()

    # 获取数据
    datalist = User.objects.all()
    # jsondata = Js
    print(datalist)
    for obj in datalist:
        print(obj.pk, obj.name)

    return HttpResponse("成功")
