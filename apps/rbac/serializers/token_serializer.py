from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import User

# 如果user没有激活，也拿不到token
class CustomObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user:User):
        token = super().get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token
    