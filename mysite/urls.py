"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path  # 为view配置url
from django.urls import include  # 将某个app中的所有url配置导入
from . import view


urlpatterns = [
    path('', view.home, name='home'),  # 主页
    path('search/', view.search, name='search' ),  # 搜索页 这里的search/ 无关紧要 可随便定义
    path('admin/', admin.site.urls),  # 默认的管理站点路由
    path('blog/', include('blog.urls', namespace='blog'))
]
    # 当直接输入网址来发起请求时,urlpatterns进行匹配'blog'并进行跳转
    # 没有命名空间依然可行,namespace的用途？？




