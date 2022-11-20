from django.urls import path
from user import views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
