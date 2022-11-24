from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import User


class CustomObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user:User):
        token = super(CustomObtainPairSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token