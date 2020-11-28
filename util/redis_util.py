import redis
import json


class RedisUtil(object):
	"""redis数据库工具"""
	def __init__(self):
		# 实例化一个连接对象
		self.client = redis.Redis() 
	
	# 有序集合
	# 获取阅读数
	def get_num_of_reading(self, post_id):
		return self.client.zscore("POST:READING_NUM", post_id)

	# 增加阅读量
	def incr_num_of_reading(self, post_id):
		# 注意顺序
		return self.client.zincrby("POST:READING_NUM", 1, post_id)	

	# 获取阅读榜单
	def get_hot_list(self):
		return self.client.zrevrange("POST:READING_NUM", 0 , 5, withscores=True)	

	# 集合 -----------------------------------------------
	# 获取点赞数
	def get_num_of_thumbs(self, post_id):
		return self.client.scard("POST:WHO_LIKES:" + str(post_id))

	# 点赞
	def incr_num_of_thumbs(self, post_id, user_id):
		self.client.sadd("POST:WHO_LIKES:" + str(post_id), user_id)

	# 取消点赞
	def decr_num_of_thumbs(self, post_id, user_id):
		self.client.srem("POST:WHO_LIKES:" + str(post_id), user_id)

	# 增加用户喜欢的文章
	def incr_post_user_like(self, post_id, user_id):
		self.client.sadd("USER:POST_LIKED:" + str(user_id), post_id)
	
	# 减少用户喜欢的文章
	def decr_post_user_like(self, post_id, user_id):
		self.client.srem("USER:POST_LIKED:" + str(user_id), post_id)

	# 判断用户是否已点赞过该文章
	def has_thumbed(self, post_id, user_id):
		return self.client.sismember("POST:WHO_LIKES:" + str(post_id), user_id)

	# 获取用户所有点赞过的文章
	def get_all_posts_user_like(self, user_id):
		return self.client.smembers("USER:POST_LIKED:" + str(user_id))

	#  ---------------- ------------------------
	# 获取收藏数
	def get_num_of_collect(self, post_id):
		return self.client.scard("POST:WHO_COLLECTS:" + str(post_id))

	# 收藏
	def incr_num_of_collect(self, post_id, user_id):
		self.client.sadd("POST:WHO_COLLECTS:" + str(post_id), user_id)

	# 取消收藏
	def decr_num_of_collect(self, post_id, user_id):
		self.client.srem("POST:WHO_COLLECTS:" + str(post_id), user_id)

	# 增加用户收藏的文章
	def incr_post_user_collect(self, post_id, user_id):
		self.client.sadd("USER:POST_COLLECTS:" + str(user_id), post_id)
	
	# 减少用户收藏的文章
	def decr_post_user_collect(self, post_id, user_id):
		self.client.srem("USER:POST_COLLECTS:" + str(user_id), post_id)

	# 判断用户是否已收藏过该文章
	def has_collected(self, post_id, user_id):
		return self.client.sismember("POST:WHO_COLLECTS:" + str(post_id), user_id)

	# 获取用户所有收藏过的文章
	def get_all_posts_user_collect(self, user_id):
		return self.client.smembers("USER:POST_COLLECTS:" + str(user_id))	

	def plus(self):
		self.client.incr("Aread")
	def add(self, address):
		self.client.ladd("address", address)