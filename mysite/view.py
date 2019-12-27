from django.shortcuts import render

from django.db.models import Q  # Q 复杂搜索
from blog.models import Post

from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger

# 定义一些零散的,全局的 视图  如  主页面


# 主页面
def home(request):
    paraments = {}
    return render(request,
                  'home.html',
                  paraments)

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

    # 符合关键字的全部帖子  # Step-1.注意 获取对象 的 __双下划线的使用
    search_posts = Post.published.filter(condition)

    # Step-2.分页机制
    paginator = Paginator(search_posts, 6)
    page = request.GET.get('page', 1)
    posts = paginator.page(page)

    # Step-3 优化显示
    current_page = posts.number;  # 当前页数
    max_page = paginator.num_pages;  # 总页数 
    
    page_range = list(range(max(current_page-2,1),min(current_page+2,max_page)+1))
    
    return render(request,
                  'blog/search.html',  
                  {
                   'search_keyword': search_keyword,
                   'posts': posts,  # 分页后的 帖子
                   'page_range':page_range,
                   })

