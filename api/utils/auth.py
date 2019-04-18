from api import models
from rest_framework.authentication import BaseAuthentication
from  rest_framework.exceptions import AuthenticationFailed
import hashlib,time

def md5(username):
    """
    生成token
    :param username:
    :return:
    """
    ctime=str(time.time())
    m=hashlib.md5(bytes(username,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))
    return m.hexdigest()



class MyAuthentication(BaseAuthentication):
    """
    封装用户认证
    """
    def authenticate(self, request):
        token=request._request.GET.get('token')
        token_obj=models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            return None
            # raise AuthenticationFailed('用户认证失败')
        return token_obj.user,token_obj

    def authenticate_header(self, request):
        pass

