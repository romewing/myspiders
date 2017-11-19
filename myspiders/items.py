# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BidedItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    owner = scrapy.Field()
    owner_phone = scrapy.Field()
