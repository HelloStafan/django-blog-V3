from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from ckeditor.fields import RichTextField  # 从ckeditor 的 字段中导入富文本字段
from taggit.managers import TaggableManager
from taggit.models import Tag


# 自定义管理器类
class PublishedManager(models.Manager):
    def get_queryset(self):  # get_queryset 为查询的具体方法，所以覆写！！
        return super(PublishedManager,  # 调用父类的构造方法
                     self).get_queryset().filter(status='published')


# Post模型类
class Post(models.Model):

    # 模型的参数
    title = models.CharField(max_length=250,
                             unique_for_date='publish') # 对于既定日期,slug有唯一性
    body = RichTextField()

    # slug = models.SlugField(max_length=250,
    #                         unique_for_date='publish')  
    # ☆创建User为Post的外键,一个User对应多个Post
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               default='lala',
                               related_name='blog_posts')

    # 帖子的时间
    publish = models.DateTimeField(default=timezone.now)
    # created = models.DateTimeField()
    # updated = models.DateTimeField()

    # 帖子的状态
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),  # 二元组?
        # 第一个元素是将存储在数据库中的值。
        # 第二个元素是将显示在窗体小部件的值。
    )
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='published')

    # 添加自定义管理器
    published = PublishedManager()
    tags = TaggableManager()  # taggit app中的管理器


    # post实例对应的url————有一个模型还能其他url吗？？
    def get_absolute_url(self):
        return reverse('blog:post_detail', # 即  url路径
                       args=[ self.publish.year,
                              self.publish.month,
                              self.publish.day,
                              self.title,
                             ])

    # 其他
    def __str__(self):
        return self.title
    class Meta:
        ordering = ('-publish',)

'''
# Comment模型类
class Comment(models.Model):
    # 定义一个外键,一个Post对应多个Comment
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,  # cascade 级联约束
                             related_name='comments')  # !!!反向查询
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)  # 自动创建
    updated = models.DateTimeField(auto_now=True)   # 自动创建

    active = models.BooleanField(default=True)  # 显示在管理站点为 勾选

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

'''





