# 架构
![架构图](./img/架构图.png)
## 5大核心组件
### Spiders(蜘蛛)
封装请求、解析数据。
### Engine(引擎)
控制整个爬虫系统的数据处理流程，并进行不同事务触发。
### Scheduler(调度器)
维护(包括去重)待爬取的URL队列，当调度程序从Scrapy Engine接受到请求时，会从待爬取的URL队列中取出下一个URL返还给他们。
### Downloader(下载器)
发送请求、获取响应
### Item Pipelines(管道)
数据清洗、持久化
# 快速开始
## 安装 pip install scrapy
## 创建项目
```
scrapy startproject demo

目录结构
./demo
├── demo
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders
│       └── __init__.py
└── scrapy.cfg
```
## 创建爬虫
```
cd demo && scrapy genspider qiu_shi www.qiushibaike.com

Created spider 'qiu_shi' using template 'basic' in module:
  demo.spiders.qiu_shi
```
```python
import scrapy


class QiuShiSpider(scrapy.Spider):
    name = 'qiu_shi'
    allowed_domains = ['www.qiushibaike.com'] # start_urls中的连接的域名必须在allowed_domains，一般不需要该属性
    start_urls = ['http://www.qiushibaike.com']

    def parse(self, response):
        pass
```
## 修改配置 settings.py
1. 关闭robots协议
```
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
```
2. 设置UserAgent
```
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
```
3. 设置日志等级为error
```
LOG_LEVEL = 'ERROR'
```
4. 开启管道功能，用于数据持久化
``` python
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'demo.pipelines.JsonWriterPipeline': 300, # 数字约小优先级越高
}
```
## 数据解析
```python
import scrapy

from demo.items import DemoItem


class QiuShiSpider(scrapy.Spider):
    name = 'qiu_shi'
    start_urls = ['https://www.qiushibaike.com/text/']

    def parse(self, response):
        divs = response.xpath("//div[contains(@id, 'qiushi_tag')]")
        for div in divs:
            auth = ''.join(div.xpath("./div/a/h2/text()").extract()).replace('\n', '')
            content = ''.join(div.xpath("./a[@class='contentHerf']/div/span/text()").extract()).replace('\n', '')
            item = DemoItem()
            item['auth'] = auth
            item['content'] = content
            yield item
```
## 运行爬虫
```
scrapy crawl qiu_shi
```
## 图片爬取
### 创建img爬虫
```
scrapy genspider img www.img.com
```
```python 
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
```
### 安装Pillow
```
pip install Pillow
```
### 修改配置
```python
ITEM_PIPELINES = {
    # 'demo.pipelines.JsonWriterPipeline': 300,
    # 'demo.pipelines.MongoPipeline': 301,
    'scrapy.pipelines.images.ImagesPipeline': 1,
}
...
IMAGES_STORE = 'images' #  图片存储位置 
```
# 爬取动态加载的数据
## selenium环境搭建
1. 安装selenium：```pip install selenium```
2. 安装[Install browser drivers](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/)
下载自己浏览器对应的版本，并设置为环境变量
3. 验证代码
```python
from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://news.163.com/domestic/")
```
## 使用下载中间件篡改返回数据
* 修改配置文件，启动下载中间件
```python
# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'demo.middlewares.DemoDownloaderMiddleware': 543,
}
```
* 编写response中间件
```python
from scrapy.http import HtmlResponse
class DemoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        if request.url in spider.start_urls:
            # 获取动态加载的新闻数据
            spider.driver.get(request.url)
            html = spider.driver.page_source  # 包含新闻数据的html页面
            return HtmlResponse(url=request.url, body=html, encoding='utf-8')
        return response
```
* 请求传参，将一个解析函数中的对象传递到下一个解析函数中
```
第一个解析函数：scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': item})
第二个解析函数：response.meta['item']
```
