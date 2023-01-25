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
    data = {
        'code': 200,
        'message': "获取成功",
        'data': preData
    }
    print("完成发送任务")
    return JsonResponse(data=data, safe=False)


@csrf_exempt
def newProject(request):
    data = json.loads(request.body)
    projectName = data['prjectName']
    print(data)
    print(projectName)
    Project.objects.create(name=projectName, status='r', addTime=datetime.datetime.now())
    print("你好ssss")
    return HttpResponse("成功")


# 保存新建的项目
@csrf_exempt
def saveProject(request):
    data = json.loads(request.body)
    print(data)
    phaseList = data["phases"]
    # 这个地方需要协商
    # lastProject = Project.objects.last()
    # projectId = lastProject.id +1
    projectId = data["projectId"]
    print(projectId)
    #
    # # 这样的话，多线程后面要加互斥锁
    # # 取数据库中最后一个元组的id
    task = Task.objects.last()
    project = Project.objects.get(id=projectId)
    initialId = task.id + 1
    print(initialId)
    initialId = 92
    print(initialId)
    ct = 1
    for phase in phaseList:
        for task in phase:
            print(1)
            ls = task['thisId']
            rb = task['fatherID']
            tmp = Task.objects.create(name=task["name"], desc="00", addTime=datetime.datetime.now(), type=1,
                                      thisId=ls,
                                      thisFarther=rb, phase=ct,
                                      startTime=datetime.datetime.now(),
                                      deadLine=datetime.datetime.now())
            # 将task和project一一关联起来
            Task_Project.objects.create(task=tmp, project=project, number=1, addTime=datetime.datetime.now())
            # 将task和user,project和user一一关联起来
            currentType = 0
            for obj in task['staffs']:
                currentType += 1
                user = User.objects.get(pk=obj)
                Task_User.objects.create(task=tmp, user=user, addTime=datetime.datetime.now(),type=currentType)
                if not Project_User.objects.filter(user_id=obj, project_id=projectId).exists():
                    Project_User.objects.create(project=project, user=user, addTime=datetime.datetime.now())
        ct += 1
        initialId += ct
    return respondDataToFront("成功")


# 根据用户id得到该用户所参加的所有项目列表
def getThisUserProjectList(request):
    thisUserId = request.GET.get("userId")
    print(thisUserId)
    projectList = Project_User.objects.filter(user=thisUserId).values("project__status",
                                                                      "project__name",
                                                                      "project__id",
                                                                      "project__addTime"
                                                                      ).distinct()
    print(projectList)
    return respondDataToFront(list(projectList))


# 根据项目的pid得到该项目下的任务列表以及各任务对应的人员分配信息
def getTasksFromTheProject(request):
    print(request.GET)
    projectId = request.GET.get("projectId")
    print(projectId)
    phases = 2
    # projectInfo = {}
    phaseList = []
    # 假定现在就两个阶段
    for phase in range(1, phases + 1):
        TaskList = Task_Project.objects.filter(project=projectId, task__phase=phase).values("task__id",
                                                                                              "task__name",
                                                                                              "task__status",
                                                                                              "task__thisId",
                                                                                              "task__thisFarther",
                                                                                              "task__phase",
                                                                                              "task__phase",
                                                                                              "task__desc",
                                                                                              "task__deadLine",
                                                                                              "task__startTime")
        phaseItem = {}
        phaseItem["phaseName"] = "Phase " + str(phase + 2)
        phaseItem["task__number"] = len(TaskList)
        userList = []
        applierList = []
        # 下面是默认两个阶段，每个阶段有若干个任务
        for task in TaskList:
            applierList.append(
                list(Task_User.objects.filter(task_id=task['task__id']).values("user__username", "type")))
        TaskList = list(TaskList)
        for i in range(len(TaskList)):
            TaskList[i]['AssignedPersons'] = applierList[i]
        # print(applierList)
        # print(TaskList)
        phaseItem["phaseTasks"] = TaskList
        phaseList.append(phaseItem)

        # projectInfo["phase"+str(phase)] = TaskList
        # projectInfo["phase"+str(phase)+"Number"] = len(TaskList)

    for item in phaseList:
        print(item)
    # print(phaseList)
    return respondDataToFront(phaseList)


@csrf_exempt
def saveTask(request):
    taskName = "阶段一任务一"
    taskType = 1  # 表示当前任务的类型
    dic = request.POST.get("userIdProcedureMap")
    # print(dic[2])
    print(request.POST.get("taskName"))
    print("这里是用户列表1111")
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
