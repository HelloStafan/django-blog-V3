'''

	自定义一些公共上下文变量

'''
from django.shortcuts import get_object_or_404 
# 相关模型
from .models import Post
from taggit.models import Tag  # 该app中的内置Tag模型

# 工具
from util.redis_util import RedisUtil  # redis工具类
from datetime import datetime
import json


redis_util = RedisUtil() 

# 获取所有标签(携带相应帖子的数量)
def get_all_tags_with_count(request):
    '''
    获取各个标签对应的帖子数量;
        参数: 由Tag对象组成的querySet
        返回: 由Tag对象组成的列表，列表以数量逆序
    '''

    # 获取所有tag
    all_tags = Tag.objects.all()  

    # ★获取标签对应帖子的数量(猴子补丁)
    for tag in all_tags:    # 注意  管理器的运用！
        tag.posts_count = Post.published.filter(tags=tag).count()

    # 按标签 对应帖子数量 排序
    tag_list = list(all_tags)   
    all_tags = sorted(tag_list, key=lambda x: x.posts_count, reverse=True)

    return {"all_tags": all_tags}

# 获取所有时间(携带相应帖子的数量)
def get_all_date_with_count(request):
    '''
    获取各个日期对应的数量;
        参数: 帖子对象集合
        返回: 字典 {日期对象：对应的帖子数量};
    '''
    all_posts = Post.published.all()  # 所有帖子

    all_date = {}
    for post in all_posts:
        # 获取 该帖子的时间
        y =  post.publish.year
        m = post.publish.month

        # 1. 创建 时间字符串,作为字典的键
        # date = "%s年%s月"%(y,m)
        
        # 2. 也可以创建 日期对象，作为字典的键
        date_obj = datetime(y, m, 1);

        # 获取 该时间的帖子数量    
        all_date[date_obj] = Post.published.filter(publish__year=y,
                                                    publish__month=m).count()
    return {"all_date": all_date}

# 获取阅读榜单
def get_hot_list(request):
    hot_list = []
    # get_hot_list方法返回一个由(帖子id，帖子阅读量)构成的列表
    for post_id,num in redis_util.get_hot_list():
        post = get_object_or_404(Post, id=post_id.decode())
        num = int(num)
        hot_list.append((post,num))
    return {"hot_list" : hot_list}

# 获取最新榜单
def get_new_list(request):
    # 按时间降序排列
    new_list = Post.published.all().order_by('-publish')[0:5] 
    return {"new_list" : new_list}