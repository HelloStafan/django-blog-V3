from django.urls import path,re_path  # url相关
from . import views

app_name = 'blog'  # 命名空间 和 url名称的用途

urlpatterns = [
    # 1.请求参数(无)      => 帖子列表(所有)
    path('', views.post_list, name='post_list'),

    # 2.请求参数(str:tag) => 帖子列表(拥有特定tag)
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    # 3.请求参数(/tag) => 标签列表(所有)
    path('tag', views.tag_list, name='tag_list'),

    # 4.请求参数(int:年月日) => 帖子详情
        # 注意：具有唯一标识性
    path('<int:year>/<int:month>/<int:day>/<str:title>',
         views.post_detail,
         name='post_detail'
         ),

]