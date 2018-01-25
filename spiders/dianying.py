# coding: utf-8
import scrapy
from fanghua.items import FanghuaItem


class DingyingSpider(scrapy.Spider):
    # 爬虫名称
    name = 'dianying'
    # 爬虫允许爬取域名
    allowed_domains = ['movie.douban.com']
    # 基础域名
    base_url = 'https://movie.douban.com/subject/26862829/comments'
    # 爬虫起始URL
    start_urls = ['https://movie.douban.com/subject/26862829/comments?status=P']
    # 爬虫页数控制初始值
    count = 1
    # 爬虫爬取页数
    spider_end = 1

    def parse(self, response):

        item = FanghuaItem()

        # 下一页地址
        nextPage = self.base_url + response.xpath("//div[@id='paginator']/a[@class='next']/@href").extract()[0]

        # 提取短评信息
        node_list = response.xpath("//div[@class='comment-item']")
        for node in node_list:
            item['content'] = node.xpath("./div[@class='comment']/p/text()").extract()[0]
            yield item


        # 爬虫页数控制及末页控制
        if self.count < self.spider_end:
            # 爬虫页数控制自增    
            self.count = self.count + 1

            # 爬取下一页
            yield scrapy.Request(nextPage, callback=self.parse)
        else:
            # 爬虫退出
            return None