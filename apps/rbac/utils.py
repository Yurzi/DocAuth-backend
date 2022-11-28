from random import Random
import hashlib
from rest_framework_simplejwt.tokens import RefreshToken


# 获取由4位随机大小写字母、数字组成的salt值
def createSalt(length=8):
    salt = ''
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+'
    len_chars = len(chars) - 1
    rnd = Random()
    for i in range(length):
        salt += chars[rnd.randint(0, len_chars)]
    return salt


# 获取原始密码+salt的md5值
def createMD5(password):
    salt='salt'
    md5 = hashlib.md5()
    md5.update(str(password + salt).encode('utf-8'))
    return md5.hexdigest()


def getTokensForUser(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }