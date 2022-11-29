import datetime
from django.http.response import JsonResponse
from django.core import serializers
from django.shortcuts import render, HttpResponse, redirect
import json
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from ..rbac.models import User
from .models import Project, Task, Task_User, Project_User, Task_Project
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


def newProject(request):
    projectName = "项目1"
    Project.objects.create(name=projectName, status='r', addTime=datetime.datetime.now())
    print("你好")
    return HttpResponse("成功")


# 保存新建的项目
@csrf_exempt
def saveProject(request):
    data = json.loads(request.body)
    print(data)
    phaseList = []
    phase1 = data["phase1"]
    phase2 = data["phase2"]
    phaseList.append(phase1)
    phaseList.append(phase2)
    projectId = data["projectId"]
    print(phase1)
    print(projectId)
    # 这样的话，多线程后面要加互斥锁
    # 取数据库中最后一个元组的id
    task = Task.objects.last()
    project = Project.objects.get(id=projectId)
    initialId = task.id + 1
    # initialId = 1
    print(initialId)
    for phase in phaseList :
        ct = 0
        for task in phase:
            ls = 0
            rb = 0
            if int(task['leftSon']) != 0 :
                ls = int(task['leftSon']) + initialId
            if int(task['rightBrother']) != 0 :
                rb = int(task['rightBrother']) + initialId
            tmp = Task.objects.create(name=task["name"], desc="00", addTime=datetime.datetime.now(), type=1,
                                      leftSon=ls,
                                      rightBrother=rb, phase=1)
            # 将task和project一一关联起来
            Task_Project.objects.create(task=tmp, project=project, number=1, addTime=datetime.datetime.now())
            #将task和user,project和user一一关联起来
            for obj in task['user']:
                user = User.objects.get(pk=obj)
                Task_User.objects.create(task=tmp,user=user,addTime=datetime.datetime.now())
                if  not Project_User.objects.filter(user_id=obj, project_id=projectId).exists():
                    Project_User.objects.create(project=project,user=user,addTime=datetime.datetime.now())
            ct += 1
        initialId += ct

    # for task in phase2:
    #     tmp = Task.objects.create(name=task["name"], desc="00", addTime=datetime.datetime.now(), type=1 ,
    #                               leftSon=int(task['leftSon']) + initialId,
    #                               rightBrother=int(task['rightBrother']) + initialId, phase=1)
    #     Project_User.objects.create(project=project, user=tmp, addTime=datetime.datetime.now())
    #     Task_Project.objects.create(task=tmp, project=project, number=1, addTime=datetime.datetime.now())

    return HttpResponse("成功")


# 根据用户id得到该用户所参加的所有项目列表
def getThisUserProjectList(request):
    thisUserId = request.GET.get("userId")
    print(thisUserId)
    projectList = Project_User.objects.filter(user=thisUserId).values_list("project__status",
                                                                           "project__name",
                                                                           "project__id",
                                                                           "project__addTime"
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
    TaskList = Task_Project.objects.filter(project=projectId).values("task__id", "task__name", "task__status",
                                                                     "task__leftSon",
                                                                     "task__rightBrother")
    userList = []
    applierList = []
    # 下面是默认两个阶段，每个阶段有若干个任务
    # print(list(Task_User.objects.filter(task_id=18).values("user__username")))
    for task in TaskList:
        applierList.append(list(Task_User.objects.filter(task_id=task['task__id']).values("user__username")))
    TaskList = list(TaskList)
    # print(TaskList)
    for i in range(len(TaskList)):
        TaskList[i]['username'] = applierList[i]
    print(applierList)
    print(TaskList)
    return respondDataToFront(TaskList)


@csrf_exempt
def saveTask(request):
    taskName = "阶段一任务一"
    taskType = 1  # 表示当前任务的类型
    dic = request.POST.get("userIdProcedureMap")
    # print(dic[2])
    print(request.POST.get("taskName"))
    print("这里是用户列表")
    userIdProcedureMap = {2: 1, 3: 2, 4: 3, 1: 4}  # 前端传递的用户项目
    pId = 1  # 由前端将数据传递过来
    project = Project.objects.get(id=pId)
    # models.task.objects.create(name=projectName, status=0, addTime=datetime.datetime.now())

    # 1保存当前任务(互斥锁需要)
    Task.objects.create(name=taskName, type=taskType)
    task = Task.objects.last()
    print(task.id)
    Task_Project.objects.create(project=project, task=task, number=0, addTime=datetime.datetime.now())

    # 2保存当前项目下的人员分工（互斥锁）
    for key in userIdProcedureMap.keys():
        userInfor = User.objects.get(id=key)
        Project_User.objects.create(project=project, user=userInfor)

    # 3保存当前任务下的人员分工(这个地方需要加锁)
    for key, value in userIdProcedureMap.items():
        userInfor = User.objects.get(id=key)
        Task_User.objects.create(task=task, user=userInfor, addTime=datetime.datetime.now())
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
