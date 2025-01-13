import redis
from redis import Redis
import time
import os
# from sam_config import REDIS, REDIS_PORT,
redis_max_connections = os.environ.get('REDIS_MAX_CONNECTIONS', 1024) #default=1024
REDIS = os.environ.get('REDIS_SERVICE', "redis") #default=redis
REDIS_PORT = os.environ.get('REDIS_PORT', 6379) #default=6379

class RedisAccess:
    def __init__(self, db_id):
        self.pool = redis.ConnectionPool(
            host='localhost',
            port=REDIS_PORT,
            #password=Config.redis_password,
            db=db_id,
            max_connections=redis_max_connections,
        )
        self.conn: Redis = redis.Redis(connection_pool=self.pool)

    def redis_get(self, key):
        start = time.time()
        result = self.conn.get(key)
        end = time.time()
        #print(f"context=redis_get||key={key}||cost={end - start}", flush=True)

        return result

    def redis_set(self, key, value, ex=None):
        start = time.time()
        result = self.conn.set(key, value, ex)
        end = time.time()
        #print(f"context=redis_set||key={key}||result={result}||cost={end - start}", flush=True)

        return result

    def redis_delete(self, key):
        start = time.time()
        self.conn.delete(key)
        end = time.time()
        #print(f"context=redis_delete||key={key}||cost={end - start}", flush=True)

    def redis_scan(self, match, count=1000):
        start = time.time()
        result = self.conn.scan(match=match, count=count)
        end = time.time()
        #print(f"context=redis_scan||match={match}||count={count}||cost={end - start}", flush=True)
        return result

    def redis_evict(self, keys):
        """淘汰掉ttl最小的key"""
        start = time.time()
        ttls = [self.conn.ttl(key) for key in keys]
        evict_key = keys[ttls.index(min(ttls))]
        self.conn.delete(evict_key)
        end = time.time()
        #print(f"context=redis_evict||key={evict_key}||cost={end - start}", flush=True)

    def redis_expire(self, key, ex):
        start = time.time()
        result = self.conn.expire(key, ex)
        end = time.time()
        #print(f"context=redis_expire||key={key}||result={result}||cost={end - start}", flush=True)

        return result

rds = RedisAccess(0)