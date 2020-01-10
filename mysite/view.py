# 导入上层目录包
import sys
sys.path.append('../')
from django.shortcuts import render

from django.db.models import Q  # Q 复杂搜索
from blog.models import Post
from blog.views import all_posts, all_tags, all_date, \
                        paginate, get_page_range

from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger

import linecache
import random
# 定义一些零散的,全局的 视图  如  主页面

def get_random_motto():
    '''
    随机获取一个语句
    '''
    # 文件路径
    # 注意这里的路径,！！??
    file_name = "./motto.txt" 
    # 随机行数
    line_number = random.randint(1,3);
    # 获取指定行数内容
    return linecache.getline(file_name, line_number)


# 主页面
def home(request):
    # 分页
    posts = paginate(all_posts, request.GET)
    # 获取页码范围
    page_range = get_page_range(posts)
    # 获取随机语句
    motto = get_random_motto()

    return render( request,
                  'home.html',
                  { # 列表信息
                   'posts':posts,
                   'page_range':page_range,
                    # 侧边栏信息    
                   'all_tags':all_tags,
                   "all_date":all_date,
                   'motto':motto,
                   })



# ★搜索页面
def search(request):
    search_keyword = request.GET.get('kw', '').strip()  # 从表单中 获取对应请求(为get请求)的kw参数

    # Step-3.分词机制
    condition = None

    for word in search_keyword.split(' '):  # 因为 分词要split，所以之前先 strip删除无效字符
        if condition is None:
            condition = Q(title__icontains=word)  # contains——部分匹配；i——不区分大小写
        else:
            condition = condition|Q(title__icontains=word)

    # Step-1获取帖子  .注意 获取对象 的 __双下划线的使用
    search_posts = Post.published.filter(condition)

    # Step-2.分页机制
    posts = paginate(search_posts, request.GET)

    # Step-3 优化显示 ———— 获取页码范围
    page_range = get_page_range(posts)
    
    return render(request,
                  'blog/search.html',  
                  {
                   'search_keyword': search_keyword,
                   'posts': posts,  # 分页后的 帖子
                   'page_range':page_range,
                   })

