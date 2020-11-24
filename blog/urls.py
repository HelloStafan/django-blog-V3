from django.urls import path,re_path  # url相关
from . import views

app_name = 'blog'  # 命名空间 和 url名称的用途

urlpatterns = [
    # 1.1 请求参数()      => 帖子列表(所有)
    path('', views.post_list, name='post_list'),

    # 1.2 请求参数(str:tag) => 帖子列表(tag)
    path('tag/<slug:tag_slug>/', views.post_list_by_tag, name='post_list_by_tag'),

    # 1.3 请求参数(str:date) => 帖子列表(date)
    path('time/<int:year>/<int:month>', views.post_list_by_date, name='post_list_by_date'),

    # 2.请求参数(/tag) => 标签列表(所有)
    path('tag', views.tag_list, name='tag_list'),

    # 3.请求参数(int:年月日&标题) => 帖子详情
        # 注意：具有唯一标识性
    path('<int:year>/<int:month>/<int:day>/<str:title>',
         views.post_detail,
         name='post_detail'
         ),

    # AJAX
    path('getPost', views.getPost),
    path('thumbUp', views.thumbUp),
    path('collect', views.collect),
    # 我的点赞、收藏
    path('ilike', views.get_all_posts_user_like, name="ilike"),
    path('icolletc', views.get_all_posts_user_colletc, name="icolletc"),
]