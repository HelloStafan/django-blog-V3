from django.shortcuts import render  # 快捷方式：渲染
from django.shortcuts import get_object_or_404  # 快捷方式：查询对象

# 分页相关
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger

# 相关模型
from .models import Post
from taggit.models import Tag  # 该app中的内置Tag模型

from markdown import markdown
from datetime import datetime


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

def get_page_range(Pageobj):
    '''
    获取页数的范围，用于展现的优化; 
        参数: 页面对象
        返回: 数量范围的列表
    '''
     # 3.优化显示 
    current_page = Pageobj.number;  # 当前页数
    max_page = Pageobj.paginator.num_pages;  # 总页数 
    
    page_range = list(range(max(current_page-2,1),min(current_page+2,max_page)+1))
    return page_range

def get_tags_with_count(tags):
    '''
    获取各个标签对应的数量;
        参数: Tag对象集合
        返回: Tag对象组成的列表，列表以数量逆序
    '''
    # ★获取标签对应帖子的数量(猴子补丁)
    for tag in tags:    # 注意  管理器的运用！
        tag.posts_count = Post.published.filter(tags=tag).count()

    # 按标签 对应帖子数量 排序
    tag_list = list(all_tags)   
    tags = sorted(tag_list, key=lambda x: x.posts_count, reverse=True)
    return tags

def get_date_with_count(posts):
    '''
    获取各个日期对应的数量;
        参数: 帖子对象集合
        返回: 字典 键为日期对象，值为对应的数量;
    '''
    all_date = {}
    for post in posts:
        # 获取 该帖子的时间
        y =  post.publish.year
        m = post.publish.month

        # 创建 时间字符串 
        # date = "%s年%s月"%(y,m)
        
        # 也可以创建 日期对象
        date_obj = datetime(y,m,1);
        # 获取 该时间的帖子数量    publish.year不可以吗？？
        
        all_date[date_obj] = Post.published.filter(publish__year=y,
                                                    publish__month=m).count()
    return all_date

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

all_tags = get_tags_with_count(all_tags)
all_date = get_date_with_count(all_posts)


# 1.1 帖子列表(all)
def post_list(request):
    
    # 分页
    posts = paginate(all_posts, request.GET)
    # 获取页码范围
    page_range = get_page_range(posts)

    return render(request,
                  'blog/post_list.html',
                  { 
                    # 列表信息
                   'posts': posts,  
                   'page_range': page_range,  
                    # 侧边栏信息    
                   'all_tags': all_tags,
                   "all_date": all_date,
                   }) 

# 1.2 帖子列表(tag)
def post_list_by_tag(request, tag_slug):

    # 获取特定内容
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = all_posts.filter(tags__in=[tag]) 
        # tags ———— Post管理器；# tags__in = [tag] 

    # 分页
    posts = paginate(posts, request.GET)
    # 获取页码范围
    page_range = get_page_range(posts)

    return render(request,
                  "blog/post_list_by_tag.html",
                  {
                    # 标题信息
                   'tag':tag,
                    # 列表信息
                   'posts':posts,
                   'page_range':page_range,
                    # 侧边栏信息    
                   'all_tags':all_tags,
                   "all_date":all_date,
                  })

# 1.3 帖子列表(date)
def post_list_by_date(request, year, month):

    # 获取特定内容
    posts = all_posts.filter(publish__year=year, publish__month=month)

    # 分页
    posts = paginate(posts, request.GET)
    # 获取页面范围
    page_range = get_page_range(posts)

    date = str(year) + "年" + str(month) + "月"

    return render(request,
                  "blog/post_list_by_date.html",
                  {
                    # 标题信息
                   'date':date,
                    # 列表信息
                   'posts':posts,
                   'page_range':page_range,
                    # 侧边栏信息    
                   'all_tags':all_tags,
                   "all_date":all_date,
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
    print(post)
    # 获取当前post的页数     
    paginator = Paginator(all_posts, 1)

    all_posts_list = list(all_posts)
    page = all_posts_list.index(post) + 1   
    

    # 获取上/下一篇     不是数字，返回第一页;数字不对，最后一页
    before_post = paginator.get_page(page + 1)
    after_post = paginator.get_page(page - 1)

    return render(request,
                  "blog/detail.html",
                  {'post':post,  # 当前帖子对象
                   'before_post': before_post,  # 前一个帖子对象
                   'after_post': after_post,  # 后一个帖子对象
                   # 侧边栏信息    
                   'all_tags': all_tags,
                   "all_date": all_date,
                   })


# 4.分类列表
def tag_list(request,):

    tags = get_tags_with_count(all_tags)
    return render(request,
                  "blog/tag.html",
                  {'tags':tags,
                   })
