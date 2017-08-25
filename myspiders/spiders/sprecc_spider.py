# -*- coding: utf-8 -*-

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class SPRECCSpider(scrapy.Spider):
    name = "sprecc"
    start_urls = ['http://www.spprec.com/sczw/jyfwpt/005001/005001003/']

    def parse(self, response):
        trs = response.xpath(
            '//div[@id="container"]//td[@class="rightmain"]/div[@class="s-con"]//tr[@height="25"]')
        for tr in trs:
            url = tr.xpath('./td[@align="left"]/a/@href').extract_first()
            if url is not None:
                next_url = response.urljoin(url)
                yield response.follow(next_url, callback=self.parse_detail)

    def parse_detail(self, response):
        content = response.xpath(
            '//epointform//table[@id="_Sheet1"]')
        text = content.extract_first()
        name = content.xpath('.//td[text()="项目及标段名称"]/following-sibling::td/text()').extract_first()
        owner = content.xpath('.//td[text()="项目业主"]/following-sibling::td/text()').extract_first()
        owner_phone = content.xpath('.//td[text()="项目业主联系电话"]/following-sibling::td/text()').extract_first()
        yield {'text': text, 'name': name, 'owner': owner, 'owner_phone': owner_phone}


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(SPRECCSpider)
    process.start()
