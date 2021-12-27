import scrapy

from demo.items import ImgItem


class ImgSpider(scrapy.Spider):
    name = 'img'
    start_urls = ['https://sc.chinaz.com/tupian/']
    scheme = "https"

    def parse(self, response):
        img_list = response.xpath("//div[@id='container']/div/div/a/img/@src2").extract()
        item = ImgItem()
        item['image_urls'] = [f"{self.scheme}:{img}" for img in img_list]
        yield item

