from django.urls import path

from .views import project

urlpatterns = [
    path('/test/', project.test),
    path('/saveProject/', project.saveProject),
    path('/saveTask/', project.saveTask),
    path('/getTasksFromTheProject/', project.getTasksFromTheProject),
    path('/getThisUserProjectList/', project.getThisUserProjectList),
    path('/newProject/', project.newProject),
]
