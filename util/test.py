from redis_util import RedisUtil
import redis

redis.Redis().zadd('test',{'a': 10, 'b': 12, 'c': 5,'d' : 20})