# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    auth = scrapy.Field()
    content = scrapy.Field()


class ImgItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
