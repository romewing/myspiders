import redis
import scrapy.dupefilters


class RedisDupeFilter(scrapy.dupefilters.BaseDupeFilter):
    def __init__(self, server, key):
        self.server = server
        self.key = key

    @classmethod
    def from_settings(cls, settings):
        redis_host = settings.get('REDIS_HOST', '127.0.0.1')
        redis_port = settings.get('REDIS_PORT', 6379)
        redis_db = settings.get('REDIS_DB', 1)
        redis_key_url = settings.get('REDIS_URL_KEY', "scrapy_url")
        return cls(redis.Redis(host=redis_host, port=redis_port, db=redis_db), redis_key_url)

    def request_seen(self, request):
        url = request.url
        if self.server.sismember(self.key, request.url):
            return True
        else:
            self.server.sadd(self.key, url)
            return False
