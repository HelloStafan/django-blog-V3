from django.db import models
from blog.models import Post 
# Create your models here.

class User(models.Model):
	

	name = models.CharField(max_length=20)
	password = models.CharField(max_length=20)


	# 点赞的文章
	post_liked = models.ManyToManyField(Post, 
										blank=True,
										related_name="all_users_liked")
	# 收藏的文章
	post_collected = models.ManyToManyField(Post, 
											blank=True,
											related_name="all_users_collected")