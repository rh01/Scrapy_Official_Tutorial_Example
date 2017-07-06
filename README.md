这篇教程是之前学习scrapy时留下的代码进行小小地改动，增加了部分的数据存储模块。

## 介绍

这个爬取的目标网站是scrapy官方项目的实验网站，也就是说官方将其用作测试和实验。因此在这里继续延续该网站的 [quotebot](https://github.com/scrapy/quotesbot) 作为蓝本造轮子。



##  必需的软件环境

- [x] anaconda3.4
- [x] mongodb
- [x] scrapy
- [x] python=3.5.2



## Let's Start Code

1. spider/quotes.py

```py
# -*- coding: utf-8 -*-
import scrapy

from quotestutorial.items import QuotesItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        item = QuotesItem()
        quotes = response.css('.quote')
        for quote in quotes:
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield (item)

        next = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)
```

这段代码主要说明了如何对目标网站进行解析和生成Item对象。

2. pipeline.py

```python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem


class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
```

主要定义了如何对解析到内容进行处理或者如何保存。

3. items.py

```py
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

```

items.py主要定义了爬取的字段。

4. settings.py

```pyth
# -*- coding: utf-8 -*-

# Scrapy settings for quotestutorial project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'quotestutorial'

SPIDER_MODULES = ['quotestutorial.spiders']
NEWSPIDER_MODULE = 'quotestutorial.spiders'

MONGO_URI = 'localhost'
MONGO_DB = 'quotestutorial'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'quotestutorial (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

....
# Enable or disable spider middlewares

# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
	'quotestutorial.pipelines.TextPipeline': 300,
    'quotestutorial.pipelines.MongoPipeline': 400,
}

```

主要定义了相关的配置，比如全局配置，设置headers，设置是否启用item_pipelines.







## How To Use 

```powershell
$ scrapy crawl quotes
```

you can see results followed.

![](http://olrs8j04a.bkt.clouddn.com/17-7-6/76627811.jpg)

![](http://olrs8j04a.bkt.clouddn.com/17-7-6/72296002.jpg)

## License

![](https://img.shields.io/packagist/l/doctrine/orm.svg)