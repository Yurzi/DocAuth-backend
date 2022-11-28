from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
# Instead of referring to User directly, you should reference the user model using django.contrib.auth.get_user_model()
# Register your models here.
