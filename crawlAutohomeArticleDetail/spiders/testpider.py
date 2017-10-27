# -*- coding: utf-8 -*-
import scrapy


class TestpiderSpider(scrapy.Spider):
    name = 'testpider'
    allowed_domains = ['www.autohome.com.cn']
    start_urls = ['http://www.autohome.com.cn/comment/Articlecomment.aspx?articleid=901670']

    def start_requests(self):
        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['istrue'] = 'False'
            yield request

    def parse(self, response):
        title = response.css('.tit_rev a::text').extract_first()
        titleurl = response.urljoin(response.css('.tit_rev a::attr(href)').extract_first())
        print('主题：', title)

        innum = titleurl.find('#')
        print(innum)
        print('主题URL：', response.urljoin(titleurl[0:innum]))
        pllist = response.css('.user-comment-list')
        print(pllist)
        # for cm in pllist:
        ##reply-item-64114601
        ##reply-list > dt:nth-child(1)
        acss = 'reply-list > dt:nth-child(%s)' % 1
        plcoments = pllist.css('dd')
        plcon=0
        for cm in plcoments:
            plcon=plcon+1

            aus= pllist.css('dt:nth-child(%s)'%plcon)
            if aus:
                print('dt:nth-child(%s)' % plcon)
                print('aus',aus)
                author= aus.css('.fn-left *::text').extract_first()
                pubtime= aus.css('.fn-right::text').extract_first()
                floor= aus.css('.fn-right .red::text').extract_first()
                print('author:',author)
                print('pubtime:',pubtime)
                print('floor:',floor)
                # print('dt=',aus)
                content=cm.css('p::text').extract_first()
                print('pl=',content.strip())
        ##reply-list > dt:nth-child(3)
        # 分页
        # next = response.css('.page .page-item-next::attr(href)').extract_first()
        # url = response.urljoin(next);
        # # logger.log(logging.INFO, '下一页:%s' % response.url)
        # yield scrapy.Request(url=url, callback=self.parse);


