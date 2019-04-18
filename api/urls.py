from django.conf.urls import url,include
from django.contrib import admin
from rest_framework import routers
from api import views

route=routers.DefaultRouter()
route.register(r'host',views.HostView)
route.register(r'vmhost',views.VHostView)
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^(?P<version>[v1|v2]+)/auth/$', views.AuthView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/host/headers/$', views.HostView.as_view({'get': 'headers'})),
    url(r'^(?P<version>[v1|v2]+)/vmhost/headers/$', views.VHostView.as_view({'get': 'headers'})),
    # 自动生成路由
    url(r'^(?P<version>[v1|v2]+)/', include(route.urls)),
    url(r'^(?P<version>[v1|v2]+)/room/$', views.RoomView.as_view({'get': 'list','post':'create'})),
    url(r'^(?P<version>[v1|v2]+)/room/(?P<pk>\d+)/$', views.RoomView.as_view({'get': 'retrieve'})),
    # url(r'^(?P<version>[v1|v2]+)/host/', views.HostView.as_view({'get': 'list','post':'create'})),
    # url(r'^(?P<version>[v1|v2]+)/vmhost/$', views.VHostView.as_view({'get': 'list','post':'create'})),
    # url(r'^(?P<version>[v1|v2]+)/vmhost/(?P<pk>\d+)/$', views.VHostView.as_view({'get': 'retrieve','delete':'destroy','put':'update','patch':'partial_update'})),
]