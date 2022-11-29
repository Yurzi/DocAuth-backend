from django.urls import path

from . import views

urlpatterns = [
    path('test', views.test),
    path('saveProject', views.saveProject),
    path('saveTask', views.saveTask),
    path('getTasksFromTheProject', views.getTasksFromTheProject),
    path('getThisUserProjectList', views.getThisUserProjectList),
    path('newProject', views.newProject),
]
