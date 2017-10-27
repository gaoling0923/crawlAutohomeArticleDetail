# -*- coding: utf-8 -*-
import scrapy


class Test2Spider(scrapy.Spider):
    name = 'test2'
    allowed_domains = ['reply.autohome.com.cn']
    start_urls = ['http://reply.autohome.com.cn/api/comments/show.json?count=50&page=44&id=901670&appid=1&datatype=jsonp&order=0&replyid=0&callback=jQuery172031458255077045116_1508065560150&_=1508068564776']
    def start_requests(self):
        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['istrue'] = 'False'
            yield request
    def parse(self, response):
        print(response.text)
