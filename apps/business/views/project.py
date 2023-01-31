from rest_framework import status
import datetime
from rest_framework.generics import CreateAPIView
from common.custom_response import CustomResponse
from common.custom_exception import CustomException
from django.http.response import JsonResponse
import json
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from ...rbac.models import User
from ..models import Project, Task, Task_User, Project_User
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
    projectDesc = data['desc']
    print(data)
    print(projectName)
    Project.objects.create(desc=projectDesc, name=projectName, status='r', addTime=datetime.datetime.now())
    
    return HttpResponse("成功")


class createProjectView(CreateAPIView):
    def post(self, request):
        '''创建项目'''
        data = request.data
        try:
            user = User.objects.get(pk=data["user"])
        except:
            raise CustomException(status_code=status.HTTP_404_NOT_FOUND, code=404, message="用户不存在")
        project = Project.objects.create(name=data["name"],desc=data["desc"])
        Project_User.objects.create(user=user,project=project)
        return CustomResponse("创建项目成功")


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

    # 根据id得到当前项目
    project = Project.objects.get(id=projectId)
    project.status = 'r'
    project.save(force_update=True)

    # initialId = task.id + 1
    # print(initialId)
    # initialId = 92
    # print(initialId)
    ct = 1
    for phase in phaseList:
        for task in phase:
            print(1)
            ls = task['thisId']
            rb = task['fatherID']
            tmp = Task.objects.create(name=task["name"], desc="00", addTime=datetime.datetime.now(),
                                      thisId=ls,
                                      thisFarther=rb, phase=ct,
                                      startTime=datetime.datetime.now(),
                                      deadLine=datetime.datetime.now(),
                                      project=project)
            # 将task和user,project和user一一关联起来
            currentType = 0
            for obj in task['staffs']:
                currentType += 1
                user = User.objects.get(pk=obj)
                Task_User.objects.create(task=tmp, user=user, addTime=datetime.datetime.now(), duty=currentType)
                if not Project_User.objects.filter(user_id=obj, project_id=projectId).exists():
                    Project_User.objects.create(project=project, user=user, addTime=datetime.datetime.now())
        ct += 1
    return respondDataToFront("成功")


# 根据当前taskid,更新有关该task所有信息
def saveTask(request):
    data = json.loads(request.body)
    print(data)
    currentTaskId = data["id"]
    staffs = data["staffs"]
    print(staffs)
    # 删除数据库task_user表中与当前task相关的所有user
    Task_User.objects.filter(task_id=currentTaskId).delete()
    # 用新数据更新task表以及在task_user新增重新分配的user关系字段
    Task.objects.filter(id=currentTaskId).update(name=data["name"], startTime=data["startTime"],
                                                 deadLine=data["deadLine"], desc=data["desc"])
    duty = 1
    taskTmp = Task.objects.get(pk=data["id"])

    for staff in staffs:
        userTmp = User.objects.get(pk=staff)
        Task_User.objects.create(addTime=datetime.datetime.now(), duty=duty, task=taskTmp, user=userTmp)
        duty += 1
    return respondDataToFront("成功")


# 根据用户id得到该用户所参加的所有项目列表
def getThisUserProjectList(request):
    thisUserId = request.GET.get("userId")
    print(thisUserId)
    projectList = Project_User.objects.filter(user=thisUserId).values("project__status","project__name","project__id","project__addTime","project__desc").distinct()
    return respondDataToFront(list(projectList))


# 根据项目的pid得到该项目下的任务列表以及各任务对应的人员分配信息
def getTasksFromTheProject(request):
    print(request.GET)
    projectId = request.GET.get("projectId")
    currentProject = Project.objects.get(pk=projectId)
    print(projectId)
    print(currentProject.phaseNumber)
    phases = currentProject.phaseNumber
    # phases = 2
    # projectInfo = {}
    phaseList = []

    for phase in range(1, phases + 1):
        TaskList = Task.objects.filter(project=currentProject, phase=phase).values(
            "id",
            "name",
            "status",
            "thisId",
            "thisFarther",
            "phase",
            "desc",
            "deadLine",
            "startTime")
        phaseItem = {}
        phaseItem["phaseName"] = "Phase " + str(phase)
        phaseItem["task__number"] = len(TaskList)
        userList = []
        applierList = []
        # 下面是默认两个阶段，每个阶段有若干个任务
        for task in TaskList:
            applierList.append(
                list(Task_User.objects.filter(task_id=task['id']).values("user_id", "user__username", "duty")))
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


def getProjectInforById(request):
    projectId = request.GET.get("projectId")
    project = Project.objects.filter(pk=projectId)
    return respondDataToFront(list(project.values()))
