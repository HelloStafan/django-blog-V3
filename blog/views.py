from django.shortcuts import render  # 快捷方式：渲染
from django.shortcuts import get_object_or_404  # 快捷方式：查询对象


# 相关模型
from .models import Post
from taggit.models import Tag  # 该app中的Tag模型(已经有了？√app中内置的)

# 分页相关
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger

all_tags = Tag.objects.all()  # 所有标签
all_posts = Post.published.all()  # 所有帖子


# 1. 帖子列表
def post_list(request, tag_slug=None):
    
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
        template_name = "post_list_by_tag.html"
    else:
        template_name = "post_list.html"
    
    # 侧边栏的 所有标签和日期
    tags = get_count_by_tag(all_tags)
    all_date = get_count_by_date(all_posts)

    return render(request,
                  'blog/' + template_name,
                  {'posts': posts,  # posts为页面对象(一页)
                   'page_range':page_range,  # 分页渲染的页数
                   'tag': tag,
                   'all_tags':all_tags,
                   "all_date":all_date,
                   }) 

# 2. 帖子详情
def post_detail(request, year, month, day, title):

    # 将QuerySet 列表化
    posts_list = list(all_posts)
    # 分页对象(以1分页)
    paginator = Paginator(posts_list, 1) 


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


# 3.分类列表
def tag_list(request,):

    tags = get_count_by_tag(all_tags)
    return render(request,
                  "blog/tag.html",
                  {'tags':tags,
                   })



def get_count_by_tag(tags):
    '''
    获取各个标签对应的数量，返回Tag对象组成的列表，列表以数量逆序
    '''
    # ★获取标签对应帖子的数量(猴子补丁)
    for tag in tags:    # 注意  管理器的运用！
        tag.posts_count = Post.published.filter(tags=tag).count()

    # 按标签 对应帖子数量 排序
    tag_list = list(all_tags)   
    tags = sorted(tag_list, key=lambda x: x.posts_count, reverse=True)
    return tags


def get_count_by_date(posts):
    '''
    获取各个日期对应的数量，返回字典:键类型为str型，值为int型
    '''
    all_date = {}
    for post in posts:
        # 获取 该帖子的时间
        y =  post.publish.year
        m = post.publish.month
        # 创建 时间字符串 
        date = "%s年%s月"%(y,m)
        # 获取 该时间的帖子数量    publish.year不可以吗？？
        count = Post.published.filter(publish__year=y,
                                      publish__month=m).count()
        all_date[date] = count;
    return all_date



''' 
以前被css样式所迫 --
    point = (len(tags)+1)//2  #
    tags_left = tags[:point]  # 因为版面原因，将数据分成2部分
    tags_right = tags[point:]  # 因为切片为视图，即复制原有对象，故将此操作移到
'''