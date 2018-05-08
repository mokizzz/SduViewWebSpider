import scrapy
import re
from items import NewsItem
from queue import Queue
from urllib.parse import urljoin


class SduViewSpider(scrapy.Spider):
    # 用于区别Spider
    name = "SduViewSpider"
    # 允许访问的域
    allowed_domains = ['view.sdu.edu.cn']
    # 爬取的起始地址
    start_urls = ['http://www.view.sdu.edu.cn/index.htm']
    # 已爬取地址md5集合
    url_md5_set = set()
    # 未爬取地址
    url_not_reach = Queue()

    # 爬取方法
    def parse(self, response):
        if response.url.startswith("http://www.view.sdu.edu.cn/info/"):
            item = NewsItem()
            for box in response.xpath('//div[@class="new_show clearfix"]/div[@class="le"]'):
                # x = box.extract()
                # a = box.xpath('.//div[@class="news_tit"]/h3/text()').extract()
                item['newsTitle'] = box.xpath('.//div[@class="news_tit"]/h3/text()').extract()[0].strip()
                item['newsUrl'] = response.url
                # item['newsClick'] = box.xpath('.//div[@class="news_tit"]/h3').extract()[0].strip()
                item['newsPublishTime'] = box.xpath('.//div[@class="news_tit"]/p/text()').extract()[0].strip()[5:]
                item['newsContent'] = box.xpath('.//div[@class="news_content"]').extract()[0].strip()
                regexp = re.compile(r'<[^>]+>', re.S)
                item['newsContent'] = regexp.sub('',item['newsContent'])    # delete html <>
                yield item
        urls = response.xpath('//a/@href').extract()
        for url in urls:
            real_url = urljoin(response.url, url)   # 将.//等简化url转化为真正的http格式url
            # md5 check
            md5_url = self.md5(real_url)
            if md5_url in self.url_md5_set:
                pass
            else:
                self.url_md5_set.add(md5_url)
                # print(md5_url)
                # if real_url.startswith('http'):
                print(real_url)
                yield scrapy.Request(real_url, callback=self.parse)

    def md5(self, val):
        import hashlib
        ha = hashlib.md5()
        ha.update(bytes(val, encoding='utf-8'))
        key = ha.hexdigest()
        return key