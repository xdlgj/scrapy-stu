import scrapy
from selenium import webdriver

from demo.items import NewsItem


class NetCaseNewSpider(scrapy.Spider):
    name = 'net_case_new'
    start_urls = ['https://news.163.com/domestic/']

    def __init__(self):
        # 实例化一个浏览器对象
        self.driver = webdriver.Chrome()

    def parse(self, response):
        a_list = response.xpath("//div[@class='ndi_main']/div//h3/a")
        for a in a_list:
            item = NewsItem()
            item['title'] = a.xpath("./text()").extract_first()
            detail_url = a.xpath("./@href").extract_first()
            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        response.meta['item']['content'] = ''.\
            join(response.xpath("//*[@id='content']/div[2]//p[not(@class='otitle')]/text()").extract())
        return response.meta['item']

    def close(self, reason):
        self.driver.quit()
