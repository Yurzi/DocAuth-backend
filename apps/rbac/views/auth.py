from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from ..models import User


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(phone=username))
            if not (user and password):
                raise Exception("User not found")
            elif user.check_password(password):
                return user
        except Exception as e:
            return None
