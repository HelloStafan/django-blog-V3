from django.shortcuts import render  # 快捷方式：渲染
from django.shortcuts import get_object_or_404  # 快捷方式：查询对象
from django.http import HttpResponse

# 分页相关
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger

# 相关模型
from .models import Post
from util.redis_util import RedisUtil  # redis工具类
from taggit.models import Tag  # 该app中的内置Tag模型

from markdown import markdown  # 渲染md
from datetime import datetime

import json

# 定义一些函数
def paginate(objs, res_parm, num=7):
    '''
    封装分页机制;  
        参数: 对象集合, 请求参数, 每页数量 ;
        返回: 页面对象
    '''
    paginator = Paginator(objs, num)  # 实例化分页器
    page = res_parm.get('page')  # 从get请求中获取页数参数
    Pageobj = paginator.get_page(page)  # 分页器获取  页面对象
    return Pageobj

def prettify_md(post):
    '''
    美化markdown:
        参数:  对象
        返回:  无
    '''
    post.body = markdown(post.body,                       
                        extensions = [
                            'markdown.extensions.extra',
                            'markdown.extensions.codehilite',
                            'markdown.extensions.toc',
                        ])

# 定义一些变量
all_tags = Tag.objects.all()  # 所有标签
all_posts = Post.published.all()  # 所有帖子

redis_util = RedisUtil() 

# 1.1 帖子列表(all)
def post_list(request):
    
    # 分页
    posts = paginate(all_posts, request.GET)

    return render(request,
                  'blog/post_list.html',
                  { 
                    # 列表信息
                   'posts': posts,  
                   }) 

# 1.2 帖子列表(tag)
def post_list_by_tag(request, tag_slug):

    # 获取特定内容
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = all_posts.filter(tags__in=[tag]) 
        # tags ———— Post管理器；# tags__in = [tag] 

    # 分页
    posts = paginate(posts, request.GET)

    return render(request,
                  "blog/post_list_by_tag.html",
                  {
                    # 标题信息
                   'tag':tag,
                    # 列表信息
                   'posts':posts,
                  })

# 1.3 帖子列表(date)
def post_list_by_date(request, year, month):

    # 获取特定内容
    posts = all_posts.filter(publish__year=year, publish__month=month)

    # 分页
    posts = paginate(posts, request.GET)

    date = str(year) + "年" + str(month) + "月"

    return render(request,
                  "blog/post_list_by_date.html",
                  {
                    # 标题信息
                   'date':date,
                    # 列表信息
                   'posts':posts,
                  })

# 2. 帖子详情
def post_detail(request, year, month, day, title):

    # 获取所请求的帖子
    post = get_object_or_404(Post, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             title=title,
                                 )
    prettify_md(post)
    # print(post)

    # 获取当前post的页数     
    paginator = Paginator(all_posts, 1)

    all_posts_list = list(all_posts)
    page = all_posts_list.index(post) + 1   
    
    # 获取上/下一篇     不是数字，返回第一页;数字不对，最后一页
    before_post = paginator.get_page(page + 1)
    after_post = paginator.get_page(page - 1)

    # 1. 阅读量增加
    # 这个方法会初始化阅读数，然后增加阅读量
    # 浮点数更改
    # 2. 点赞数获取
    num_of_reading = int(redis_util.incr_num_of_reading(post.id))
    num_of_thumbs = int(redis_util.get_num_of_thumbs(post.id))

    return render(request,
                  "blog/detail.html",
                  {'post':post,  # 当前帖子对象,
                   'num_of_reading':num_of_reading,
                   'num_of_thumbs':num_of_thumbs,
                   'before_post': before_post,  # 前一个帖子对象
                   'after_post': after_post,  # 后一个帖子对象
                   })

# 3. 分类列表
def tag_list(request,):
    return render(request, "blog/tag.html", {})

# AJAX
def getPost(request):

    # 1. 获取参数 
    page = int(request.GET.get('page'))
    tag = request.GET.get('tag')
    year = request.GET.get('year')
    month = request.GET.get('month')

    # 2. 根据参数tag,time的有无，获取帖子
    posts = Post.published.all()
    if tag != 'undefined':
        tag = get_object_or_404(Tag, slug=tag)
        posts = Post.published.all().filter(tags__in=[tag])
    elif year != 'undefined':
        posts = Post.published.all().filter(publish__year=year, publish__month=month)
    
    # 2. 根据参数page，截取帖子(每次7条)
    request_posts = posts[(page-1)*7:page*7-1]  # 注意切片机制
    if not request_posts:  # 如果 是空的，直接返回
        return HttpResponse('[]')

    # 3. 处理帖子信息
    # querySet.values() → 一个字典列表
    resquest_posts_info = request_posts.values()

    # 循环需要处理的数据
    # 1. 时间 → 字符串 2. tag信息 3. post的详情url

    i = 0  # 需要一个索引
    for post_info in resquest_posts_info:
        post_info['publish'] = post_info['publish'].strftime('%Y-%m-%d %H:%M')

        post_info['url'] = request_posts[i].get_absolute_url()  

        # 根据索引，循环Post对象，获取其所有tag
        tags = []
        for tag in request_posts[i].tags.all():
            tags.append(str(tag))
        # 将tag字符串添加进字典
        post_info['tags'] = tags  
        i += 1

    return HttpResponse(json.dumps(list(resquest_posts_info))) 
    
def thumbUp(request):

    # 是否是点赞
    flag = request.GET.get('flag')
    post_id = request.GET.get('postId') 

    if flag == "true":
        now_thumbs = redis_util.incr_num_of_thumbs(post_id, 1)    
    else:
        now_thumbs = redis_util.incr_num_of_thumbs(post_id, -1)    
   
    return HttpResponse(json.dumps({"now_thumbs": now_thumbs}))