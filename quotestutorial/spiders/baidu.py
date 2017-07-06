# -*- coding: utf-8 -*-
import scrapy


class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["www.zhujiwu.com"]
    start_urls = ['http://www.zhujiwu.com/']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Accept-Language': 'en',
        }
    }

    def make_requests_from_url(self, url):
        return scrapy.Request(url=url, callback=self.parse_index)

    def parse_index(self, response):
        self.logger.info(response.status)

    # def parse(self, response):
    #     pass
