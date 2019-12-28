from django.shortcuts import render  # 快捷方式：渲染
from django.shortcuts import get_object_or_404  # 快捷方式：查询对象


# 相关模型
from .models import Post
from taggit.models import Tag  # 该app中的Tag模型(已经有了？√app中内置的)

# 分页相关
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger

all_tags = Tag.objects.all()
all_posts = Post.published.all() 

# 1. 帖子列表
def post_list(request, tag_slug=None):
    # 获取所有的帖子实例
    object_list = Post.published.all()
    
    # 1.添加标签机制(如果有参数tag)
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
                        # 注意tag_in!!s ———— Post管理器；
                        # tags__in = [tag] !!？？
        posts = all_posts.filter(tags__in=[tag])  
    else:
        posts = all_posts

    # 2.添加分页机制
    paginator = Paginator(posts, 6)  # 实例化分页器
    page = request.GET.get('page')  # 从get请求中获取页数参数
    posts = paginator.get_page(page)  # 分页器获取  请求页内容

    # 3.优化显示 
    current_page = posts.number;  # 当前页数
    max_page = paginator.num_pages;  # 总页数 
    
    page_range = list(range(max(current_page-2,1),min(current_page+2,max_page)+1))

    # 4.构建对象，保存其他需要显示的零散信息(如 页面的标题)
    # 以里两个文件来显示
    if tag:
        template_file = "post_list_by_tag.html"
    else:
        template_file = "post_list.html"
    
    return render(request,
                  'blog/' + template_file,
                  {'posts': posts,  # posts为页面对象(一页)
                   'page_range':page_range,  # 分页渲染的页数
                   'tag': tag,
                   'all_tags':all_tags,
                   }) 

# 2. 帖子详情
def post_detail(request, year, month, day, title):

    # 将QuerySet 列表化
    posts_list = list(all_posts)
    # 分页对象
    paginator = Paginator(posts_list, 1)  # 实例化分页器（注意后面这个参数）


    # 获取所请求的帖子
    post = get_object_or_404(Post, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             title=title,
                             )
    

    page = posts_list.index(post)+1  # 当前页

    before_object = paginator.get_page(page-1)
    after_object = paginator.get_page(page+1)

    return render(request,
                  "blog/detail.html",
                  {'post':post,  # 该页显示  1.帖子详情
                   'Before_object': before_object,  # 前一页的帖子对象
                   'After_object': after_object,  # 后一页的帖子对象
                   })


# 3.所有帖子的分类
def tag_list(request,):

    # ★获取标签对应帖子的数量(猴子补丁)
    for tag in all_tags:                       # 注意  管理器的运用！
        tag.posts_count = Post.published.filter(tags=tag).count()  # Post 模型中已有tag属性？！
    
    # 按标签 对应帖子数量 排序
    # tags = sorted(list(tags), key=lambda x : x.posts_count)
    tags_list = list(all_tags)
    tags = sorted(tags_list, key=lambda x : x.posts_count,reverse=True)

    return render(request,
                  "blog/tag.html",
                  {'tags':tags,
                  
                   })

''' 
以前被css样式所迫 --
    point = (len(tags)+1)//2  #
    tags_left = tags[:point]  # 因为版面原因，将数据分成2部分
    tags_right = tags[point:]  # 因为切片为视图，即复制原有对象，故将此操作移到
'''