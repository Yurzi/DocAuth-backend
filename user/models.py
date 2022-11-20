from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    addTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " with " + self.username
