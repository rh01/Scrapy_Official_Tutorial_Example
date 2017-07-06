# -*- coding: utf-8 -*-
import scrapy


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = ['http://www.zhihu.com/']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS':{
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Accept-Language': 'en',
        }
    }

    def __init__(self, mongo_uri=None, mongo_db=None, *args, **kwargs):
        super(ZhihuSpider, self).__init__(*args, **kwargs)
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )



    def parse(self, response):
        pass
