from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from ..serializers.token import CustomObtainPairSerializer


class CustomObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomObtainPairSerializer
