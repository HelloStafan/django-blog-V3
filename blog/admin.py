from django.contrib import admin
from .models import Post

# Register your models here.
# 管理站点：需注册模型

# admin.site.register(Post)  # 1.普通方法注册


@admin.register(Post)   # 2.利用装饰器注册———— 不用site??
class PostAdmin(admin.ModelAdmin):  # 如何装饰一个类？
	list_display = ('title','status',)
	list_filter = ('status', 'publish')

