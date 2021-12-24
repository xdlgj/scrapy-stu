import scrapy

from demo.items import DemoItem


class QiuShiSpider(scrapy.Spider):
    name = 'qiu_shi'
    start_urls = ['https://www.qiushibaike.com/text']
    prefix_url = 'https://www.qiushibaike.com'

    def parse(self, response):
        divs = response.xpath("//div[contains(@id, 'qiushi_tag')]")
        for div in divs:
            auth = ''.join(div.xpath("./div/a/h2/text()").extract()).replace('\n', '')
            content = ''.join(div.xpath("./a[@class='contentHerf']/div/span/text()").extract()).replace('\n', '')
            item = DemoItem()
            item['auth'] = auth
            item['content'] = content
            yield item
        next_uri = response.xpath("//ul[@class='pagination']/li[last()]/a/@href")
        if next_uri:  # 存在下一页则继续爬取
            yield scrapy.Request(f"{self.prefix_url}{next_uri.extract_first()}")

