from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from ..serializers.token_serializer import CustomObtainPairSerializer


class CustomObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomObtainPairSerializer
