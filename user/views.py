from rest_framework.decorators import action
from rest_framework import viewsets, status
from common.custom_exception import CustomException
from common.custrom_response import decorateRes
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return decorateRes(super().create(request, *args, **kwargs))
