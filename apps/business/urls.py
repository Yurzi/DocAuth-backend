from django.urls import path

from .views import project

urlpatterns = [
    path('saveProject', project.saveProject),
    path('getTasksFromTheProject', project.getTasksFromTheProject),
    path('saveTask', project.saveTask),
    path('/getThisUserProjectList/', project.getThisUserProjectList),
    path('/newProject/', project.newProject),
]
