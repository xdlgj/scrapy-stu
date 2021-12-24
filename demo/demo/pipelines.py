# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import pymongo

from itemadapter import ItemAdapter


class JsonWriterPipeline:

    def open_spider(self, spider):
        """
        打开爬虫的时候执行,在parse函数之前
        :param spider:
        :return:
        """
        # 这行代码可以放在__init__函数中执行
        self.file = open('qiu_shi.jl', 'w')

    def process_item(self, item, spider):
        line = f"{json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False)}\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


class MongoPipeline:

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        该方法方法是一个类方法，它的参数是crawler，通过crawler对象，我们可以拿到Scrapy的所有核心组件，
        如全局配置的每个信息，然后创建一个Pipeline实例。参数cls就是Class，最后返回一个Class实例。
        :param crawler:
        :return:
        """
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item

    def close_spider(self, spider):
        self.client.close()