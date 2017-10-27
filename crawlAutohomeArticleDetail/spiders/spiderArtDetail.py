# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
import time

from crawlAutohomeArticleDetail.items import articleItem
import logging
logger = logging.getLogger('spiderArtDetail')
class SpiderarticleSpider(scrapy.Spider):
    name = 'spiderArtDetail'
    allowed_domains = ['www.autohome.com.cn']
    start_urls = ['http://www.autohome.com.cn/4069/0/0-0-1-0/']

    def __init__(self):
        self.count=0

    def start_requests(self):
        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.topicParse)
            request.meta['istrue'] = 'False'
            yield request

    def parse(self, response):
        # response.text
        logger.log(logging.INFO, '当前页面：%s' % response.url)
        self.count=self.count+1

        subtitle= response.css('div.content  div.subnav  div.subnav-title  div.subnav-title-name  a::text').extract_first()
        print(subtitle)
        coments= response.css('#maindiv  div.tab-content-cover  div  div.cont-info  ul  li')
        # print(coments)
        for coment in coments:
            item = articleItem()
            topicurl = coment.css('.newpic a::attr(href)').extract_first()  # 主题
            turl = response.urljoin(topicurl)
            #使用正则匹配-all.hmtl
            titleURL = ''
            p = re.compile('(-)\d+(.html$)')
            if re.search(p,turl):
                titleURL = re.sub(p, '-all.html', turl)
                # print(purl)
            else:
                titleURL=turl
            print(titleURL)
            # yield scrapy.Request(url=purl, callback=self.topicParse)
            # dd = scrapy.Request(url=purl, callback=self.topicParse)
            # print(dd)
            title = coment.css('h3 a::text').extract_first()  # 主题

            crawldate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # item['title'] = title
            # item['titleURL'] = titleURL
            # item['crawldate'] = crawldate
            # item['subtitle'] = subtitle

            request= scrapy.Request(url=titleURL, callback=self.topicParse)
            request.meta['istrue'] = 'False'
            yield  request
        # logger.info()
        logger.log(logging.INFO, '文章主题：%s'% title)
        logger.log(logging.INFO, '当前页数:%s'% self.count)
        logger.log(logging.INFO, '文章主题所在URL:%s' % response.url)




        #分页
        # next = response.css('.page .page-item-next::attr(href)').extract_first()
        # url = response.urljoin(next);
        # logger.log(logging.INFO, '下一页:%s' % response.url)
        # yield scrapy.Request(url=url, callback=self.parse);
    def topicParse(self,response):
        # print('111111111111')
        logger.log(logging.INFO, '进入文章内容URL:%s' % response.url)
        # item= response.meta['item']
        plhref=response.css('#reply-all-btn1::attr(href)').extract_first()
        # nurl = next.strip() if next  else '';
        plurl = response.urljoin(plhref);
        request= scrapy.Request(url=plurl, callback=self.detailParse);
        request.meta['istrue']='True'
        yield request

        # return  coment
    def detailParse(self,response):

        logger.log(logging.INFO, '进入文章评论URL:%s' % response.url)
        title = response.css('.tit_rev a::text').extract_first()
        titleurl = response.urljoin(response.css('.tit_rev a::attr(href)').extract_first())
        print('主题：',title)

        innum=titleurl.find('#')
        print(innum)
        print('主题URL：', response.urljoin(titleurl[0:innum]))
        pllist = response.css('.user-comment-list').extract()
        # for cm in pllist:
        ##reply-item-64114601
        ##reply-list > dt:nth-child(1)
        acss='reply-list > dt:nth-child(%s)'% 1
        plcoments=pllist.css('dd P').extract()
        for cm in plcoments:
            print(cm.strip())




    def _wait(self):
        for i in range(0, 3):
            print('.' * (i % 3 + 1))
            time.sleep(1)


