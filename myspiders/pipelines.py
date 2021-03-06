# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from kafka import KafkaProducer
import json


class RabbitMQPipeline(object):
    def process_item(self, item, spider):
        return item


class KafkaPipeline(object):
    def __init__(self, kafka_topic, kafka_host):
        self.kafka_topic = kafka_topic
        self.kafka_host = kafka_host
        self.producer = None

    def process_item(self, item, spider):
        result = self.producer.send(self.kafka_topic, value=dict(item))
        type(spider)
        print(result)
        return item

    def open_spider(self, spider):
        self.producer = KafkaProducer(bootstrap_servers=self.kafka_host,
                                      value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('UTF-8'))

    def close_spider(self, spider):
        self.producer.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            kafka_topic=crawler.settings.get('KAFKA_TOPIC', 'scrapy_kafka_item'),
            kafka_host=crawler.settings.get('KAFKA_HOST', ['192.168.3.52:9092'])
        )
