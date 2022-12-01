from django.urls import path,re_path

from . import views

urlpatterns = [
    path('test', views.test),
    path('saveProject', views.saveProject),
    path('saveTask', views.saveTask),
    path('getTasksFromTheProject', views.getTasksFromTheProject),
    path('getThisUserProjectList', views.getThisUserProjectList),
    #------------------------------------
    path('/project/',views.ProjectView.as_view()),
    re_path('/project/(\d+)',views.ProjectdetailView.as_view()),
    path('/task/',views.TaskView.as_view()),
    re_path('/task/(\d+)',views.TaskdetailView.as_view()),
    path('/article/',views.ArticleView.as_view()),
    re_path('/article/(\d+)',views.ArticledetailView.as_view()),
    path('/record/',views.RecordView.as_view()),
    re_path('/record/(\d+)',views.RecorddetailView.as_view()),
    path('/project_User/',views.Project_UserView.as_view()),
    re_path('/project_User/(\d+)',views.Project_UserdetailView.as_view()),

    path('/task_project/',views.Task_ProjectView.as_view()),
    re_path('/task_project/(\d+)',views.Task_ProjectdetailView.as_view()),

    path('/task_user/',views.Task_UserView.as_view()),
    re_path('/task_user/(\d+)',views.Task_UserdetailView.as_view()),
    
]
