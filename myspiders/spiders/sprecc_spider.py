import scrapy
import redis
from scrapy.crawler import CrawlerProcess


class SPRECCSpider(scrapy.Spider):
    name = "sprecc"
    start_urls = ['http://www.spprec.com/sczw/jyfwpt/005001/005001003/']
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def parse(self, response):
        trs = response.xpath(
            '//div[@id="container"]//td[@class="rightmain"]/div[@class="s-con"]//tr[@height="25"]')
        for tr in trs:
            url = tr.xpath('./td[@align="left"]/a/@href').extract_first()
            if url is not None:
                next_url = response.urljoin(url)
                yield response.follow(next_url, callback=self.parse_detail)

    def parse_detail(self, response):
        detail = response.xpath('//epointform').extract_first()
        print(detail)
        pass

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(SPRECCSpider)
    process.start()