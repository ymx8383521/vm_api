from django.shortcuts import render
from rest_framework.views import APIView
from api import models
from rest_framework.response import Response
from api.utils.auth import MyAuthentication
from api.utils.auth import md5
from api.utils.headers import get_headers
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from api.utils.serializer import PhysicalMachineSerializer
from api.utils.serializer import VirtualMachineSerializer
from api.utils.serializer import MachineRoomSerializer
from  rest_framework.decorators import api_view,authentication_classes
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class AuthView(APIView):
    # authentication_classes = [MyAuthentication,]
    def post(self,request,*args,**kwargs):
        ret={'code':1000,'msg':''}
        try:
            user=request.data.get('username')
            pwd=request.data.get('password')
            user_obj=models.UserInfo.objects.filter(username=user,password=pwd).first()
            if not user_obj:
                ret['code']=1001
                ret['msg']='用户名或密码错误'
            else:
                token=md5(user)
                models.UserToken.objects.update_or_create(user=user_obj,defaults={'token':token})
                ret['token']=token
        except Exception as e:
            ret['code']=1002
            ret['msg']='请求异常:%s' % e
        return Response(ret)


class RoomView(ModelViewSet):
    queryset = models.MachineRoom.objects.all().order_by('id')
    serializer_class = MachineRoomSerializer
    pagination_class = PageNumberPagination


class HostView(ModelViewSet):
    queryset = models.PhysicalMachine.objects.filter(host_active=1).all()
    serializer_class = PhysicalMachineSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('host_ip',)

    def headers(self,request,*args,**kwargs):
        header_fields_list = models.PhysicalMachine._meta.fields
        header_dic=get_headers(header_fields_list)
        return Response(header_dic)



class VHostView(ModelViewSet):
    queryset = models.VirtualMachine.objects.all().select_related()
    serializer_class = VirtualMachineSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields=('vm_installed',)

    def headers(self,request,*args,**kwargs):
        header_fields_list = models.VirtualMachine._meta.fields
        header_dic=get_headers(header_fields_list)
        return Response(header_dic)

    # authentication_classes = ['MyAuthentication',]
    # @api_view(['update'])
    # @authentication_classes((MyAuthentication,))
    # def update(self, request, *args, **kwargs):
    #     pass




