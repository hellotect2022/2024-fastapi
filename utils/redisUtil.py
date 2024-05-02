import redis
from setting.Settings import Settings
from utils.logUtil import LogHelper

settings = Settings()
logHelper = LogHelper()

class RedisHelper:
    rd = None
    @classmethod
    def init_redis(self):
        if self.rd is None:
            # CONNETC REDIS
            try:
                self.rd = redis.StrictRedis(host=settings.redis_host, port=int(settings.redis_port), db=0)
                self.rd.ping()
            except redis.exceptions.ConnectionError as e:
                # 예외를 로그에 기록
                logHelper.logger.error(e)
                #raise redis.ConnectionError("Failed to connect to Redis")

    # key-value
    @staticmethod
    def setKey(key:str, value:str):
        RedisHelper.init_redis()
        RedisHelper.rd.set(key,value)

    @staticmethod
    def getKey(key):
        RedisHelper.init_redis()
        return RedisHelper.rd.get(key)

    # key-map
    @staticmethod
    def setHashMap(key,data):
        RedisHelper.init_redis()
        return RedisHelper.rd.hmset(key, data)

    @staticmethod
    def getHashMap(key,mapKey=None):
        RedisHelper.init_redis()
        redisHash = {}
        if mapKey :
            redisHash = RedisHelper.rd.hget(key,mapKey)
        else :
            redisHash = RedisHelper.rd.hgetall(key)
            resultData = {key.decode('utf-8'): value.decode('utf-8') for key, value in redisHash.items()}
        return resultData