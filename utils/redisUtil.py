import redis
from setting.Settings import Settings
from utils.logUtil import LogHelper

settings = Settings()

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
                LogHelper.error(e)

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

    @staticmethod
    def getSmembers(roomId):
        RedisHelper.init_redis()
        redisHash = {}
        redisHash = RedisHelper.rd.smembers(roomId)
        resultData = {user.decode('utf-8') for user in redisHash}
        return resultData

    @staticmethod
    def publish(redisChannel:str, message:str):
        RedisHelper.init_redis()
        RedisHelper.rd.publish(channel=redisChannel, message=message)