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
