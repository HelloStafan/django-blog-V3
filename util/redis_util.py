import redis
import json


class RedisUtil(object):
	"""docstring for RedisUtil"""
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


	# 获取点赞数
	def get_num_of_thumbs(self, post_id):

		if self.client.zscore("POST:THUMBS_NUM", post_id):
			return self.client.zscore("POST:THUMBS_NUM", post_id)
		# 如果 获取不到值
		else:
			return self.client.zincrby("POST:THUMBS_NUM", 0, post_id)

	# 增加点赞数
	def incr_num_of_thumbs(self, post_id, change):
		# 注意顺序
		return self.client.zincrby("POST:THUMBS_NUM", change, post_id)


	# 哈希表不适合进行统计，排序, 故先不用
	# def get_num_of_reading(self, post_id):
	# 	return self.client.hget("POST:READING_NUM", post_id)

	# def incr_num_of_reading(self, post_id):
	# 	return self.client.hincrby("POST:READING_NUM", post_id, 1)