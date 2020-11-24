from django.urls import path,re_path  # url相关
from . import views

app_name = 'login'  

urlpatterns = [
    path('', views.dowhat),
    path('login', views.login),
    path('register', views.register),
    path('loginout', views.login_out),
]