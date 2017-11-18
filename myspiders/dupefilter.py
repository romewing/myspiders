import redis
import scrapy.dupefilters
import time


class RedisSetDupeFilter(scrapy.dupefilters.BaseDupeFilter):
    def __init__(self, server, key):
        self.server = server
        self.key = key

    @classmethod
    def from_settings(cls, settings):
        redis_host = settings.get('REDIS_HOST', '127.0.0.1')
        redis_port = settings.get('REDIS_PORT', 6379)
        redis_db = settings.get('REDIS_DB', 1)
        redis_key_url = settings.get('REDIS_URL_KEY', "scrapy_url_")
        return cls(redis.Redis(host=redis_host, port=redis_port, db=redis_db), redis_key_url)

    def request_seen(self, request):
        #request = request_fingerprint(request)
        spider = request.meta['spider']
        if spider is not None:
            url = request.url
            key = self.key+spider
            if self.server.sismember(key, url):
                return True
            else:
                self.server.sadd(key, url)
                return False


class RedisSortedSetDupeFilter(scrapy.dupefilters.BaseDupeFilter):

    def __init__(self, server, prefix):
        self.server = server
        self.prefix = prefix

    @classmethod
    def from_settings(cls, settings):
        redis_host = settings.get('REDIS_HOST', '127.0.0.1')
        redis_port = settings.get('REDIS_PORT', 6379)
        redis_db = settings.get('REDIS_DB', 0)
        redis_key_prefix = settings.get('REDIS_URL_KEY', "scrapy_url_")
        return cls(redis.Redis(host=redis_host, port=redis_port, db=redis_db), redis_key_prefix)

    def request_seen(self, request):
        spider = request.meta['spider']
        if spider is not None:
            url = request.url
            key = self.prefix+spider
            if self.server.zrank(key, url) is not None:
                return True
            else:
                self.server.zadd(key, url, time.time())
                return False
