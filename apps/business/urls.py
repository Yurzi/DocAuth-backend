from django.urls import path,re_path

from . import views

urlpatterns = [
    path('test', views.test),
    path('saveProject', views.saveProject),
    path('saveTask', views.saveTask),
    path('getTasksFromTheProject', views.getTasksFromTheProject),
    path('getThisUserProjectList', views.getThisUserProjectList),
    #------------------------------------
    path('/Project/',views.ProjectView.as_view()),
    re_path('Project/(\d+)',views.ProjectdetailView.as_view()),
    path('Task',views.TaskView.as_view()),
    re_path('Task/(\d+)',views.TaskdetailView.as_view()),
    path('Article',views.ArticleView.as_view()),
    re_path('Article/(\d+)',views.ArticledetailView.as_view()),
    path('Record',views.RecordView.as_view()),
    re_path('Record/(\d+)',views.RecorddetailView.as_view()),
    path('Project_User',views.Project_UserView.as_view()),
    re_path('Project_User/(\d+)',views.Project_UserdetailView.as_view()),

    path('Task_Project',views.Task_ProjectView.as_view()),
    re_path('Task_Project/(\d+)',views.Task_ProjectdetailView.as_view()),

    path('Task_User',views.Task_UserView.as_view()),
    re_path('Task_User/(\d+)',views.Task_UserdetailView.as_view()),
    
]
