from django.urls import path

from .views import project,task

urlpatterns = [

    path('saveProject', project.saveProject),
    path('getTasksFromTheProject', project.getTasksFromTheProject),
    path('saveTask', project.saveTask),
    path('/getThisUserProjectList/', project.getThisUserProjectList),
    path('/newProject/', project.newProject),
    path('/task/<int:pk>', task.TaskView.as_view()),
    path('/record/list', task.RecordListView.as_view()),
    path('/usertask/list', task.Task_UserListViews.as_view()),
    path('/task/submit/<int:pk>', task.SubmitTaskView.as_view()),

]
