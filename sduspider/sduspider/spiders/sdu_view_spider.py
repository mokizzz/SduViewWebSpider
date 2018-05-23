import scrapy
import re
import requests
import pickle
from items import NewsItem
from urllib.parse import urljoin


class SduViewSpider(scrapy.Spider):
    # 用于区别Spider
    name = "SduViewSpider"
    # 允许访问的域
    allowed_domains = ['view.sdu.edu.cn']
    # 爬取的起始地址
    start_urls = ['http://www.view.sdu.edu.cn/index.htm']
    # 将要爬取的地址列表
    destination_list = start_urls
    # 已爬取地址md5集合
    url_md5_seen = []
    # 断点续爬计数器
    counter = 0
    # 保存频率，每多少次爬取保存一次断点
    save_frequency = 50

    # 重写init
    def __init__(self):
        super
        # 读取已保存的断点
        import os
        if not os.path.exists('./pause/'):
            os.mkdir('./pause/')
        if not os.path.isfile('./pause/response.seen'):
            f = open('./pause/response.seen', 'wb')
            f.close()
        if not os.path.isfile('./pause/response.dest'):
            f = open('./pause/response.dest', 'wb')
            f.close()

        f = open('./pause/response.seen', 'rb')
        if os.path.getsize('./pause/response.seen') > 0:
            self.url_md5_seen = pickle.load(f)
        f.close()
        f = open('./pause/response.dest', 'rb')
        if os.path.getsize('./pause/response.dest') > 0:
            self.start_urls = pickle.load(f)
            self.destination_list = self.start_urls
        f.close()

        # shelve存取法造成了重复存储，存储文件高达1G，因此不予采用，改用pickle法
        # response_seen = shelve.open('./pause/response.seen')
        # if len(response_seen.dict) > 0:
        #     self.url_md5_seen = response_seen['seen_list']
        # response_seen.close()

        # response_destination = shelve.open('./pause/response.dest')
        # if len(response_destination.dict) > 0:
        #     self.start_urls = response_destination['destination_list']
        #     self.destination_list = response_destination['destination_list']
        # response_destination.close()

        self.counter += 1

    # 爬取方法
    def parse(self, response):

        # 断点续爬功能之保存断点
        self.counter_plus()

        # 爬取当前网页
        print('start parse : ' + response.url)
        self.destination_list.remove(response.url)
        if response.url.startswith("http://www.view.sdu.edu.cn/info/"):
            item = NewsItem()
            for box in response.xpath('//div[@class="new_show clearfix"]/div[@class="le"]'):
                # article title
                item['newsTitle'] = box.xpath('.//div[@class="news_tit"]/h3/text()').extract()[0].strip()

                # article url
                item['newsUrl'] = response.url
                item['newsUrlMd5'] = self.md5(response.url)

                # article click time
                item['newsClick'] = box.xpath('.//div[@class="news_tit"]/p/span/script/text()').extract()[0].strip()
                pattern = re.compile(r'\(.*?\)')
                parameters = re.search(pattern, item['newsClick']).group(0)
                parameters = parameters[1:-1].split(',')
                parameters[0] = re.search(re.compile(r'\".*?\"'), parameters[0]).group(0)[1:-1]
                parameters[1] = parameters[1].strip()
                parameters[2] = parameters[2].strip()
                request_url = 'http://www.view.sdu.edu.cn/system/resource/code/news/click/dynclicks.jsp'
                request_data = {'clicktype': parameters[0], 'owner': parameters[1], 'clickid': parameters[2]}
                request_get = requests.get(request_url, params=request_data)
                item['newsClick'] = request_get.text

                # article publish time
                item['newsPublishTime'] = box.xpath('.//div[@class="news_tit"]/p[not(@style)]/text()').extract()[0].strip()[5:]

                # article content
                item['newsContent'] = box.xpath('.//div[@class="news_content"]').extract()[0].strip()
                regexp = re.compile(r'<[^>]+>', re.S)
                item['newsContent'] = regexp.sub('',item['newsContent'])    # delete templates <>

                # 索引构建flag
                item['indexed'] = 'False'

                # yield it
                yield item

        # 获取当前网页所有url并宽度爬取
        urls = response.xpath('//a/@href').extract()
        for url in urls:
            real_url = urljoin(response.url, url)   # 将.//等简化url转化为真正的http格式url
            if not real_url.startswith('http://www.view.sdu.edu.cn'):
                # and not real_url.startswith('http://view.sdu.edu.cn')
                continue    # 保持爬虫在view.sdu.edu.cn之内
            if real_url.endswith('.jpg') or real_url.endswith('.pdf'):
                continue    # 图片资源不爬
            if '.jsp?' in real_url:
                continue    # 动态网站不爬，太tm多了
            # md5 check
            md5_url = self.md5(real_url)
            # assert (self.binary_md5_url_search(md5_url) == -1) ^ (md5_url in self.url_md5_seen)
            if self.binary_md5_url_search(md5_url) > -1:    # 存在当前MD5
                pass
            else:
                self.binary_md5_url_insert(md5_url)
                # print(md5_url)
                # if real_url.startswith('http'):
                    # print(real_url)
                self.destination_list.append(real_url)
                yield scrapy.Request(real_url, callback=self.parse, errback=self.errback_httpbin)

    def md5(self, val):
        import hashlib
        ha = hashlib.md5()
        ha.update(bytes(val, encoding='utf-8'))
        key = ha.hexdigest()
        return key



    # counter++，并在合适的时候保存断点
    def counter_plus(self):
        print('待爬取网址数：' + (str)(len(self.destination_list)))
        # 断点续爬功能之保存断点
        if self.counter % self.save_frequency == 0:  # 爬虫经过save_frequency次爬取后
            print('Rayiooo：正在保存爬虫断点....')

            f = open('./pause/response.seen', 'wb')
            pickle.dump(self.url_md5_seen, f)
            f.close()

            f = open('./pause/response.dest', 'wb')
            pickle.dump(self.destination_list, f)
            f.close()

            # 弃用的shelve存储法
            # response_seen = shelve.open('./pause/response.seen')
            # response_seen['seen_list'] = self.url_md5_seen
            # response_seen.close()
            #
            # response_destination = shelve.open('./pause/response.dest')
            # response_destination['destination_list'] = self.destination_list
            # response_destination.close()

            self.counter = self.save_frequency

        self.counter += 1  # 计数器+1

    # scrapy.request请求失败后的处理
    def errback_httpbin(self, failure):
        self.destination_list.remove(failure.request._url)
        print('Error 404 url deleted: ' + failure.request._url)
        self.counter_plus()

    # 二分法md5集合排序插入self.url_md5_set--16进制md5字符串集
    def binary_md5_url_insert(self, md5_item):
        low = 0
        high = len(self.url_md5_seen)
        while (low < high):
            mid = (int)(low + (high - low) / 2)
            if self.url_md5_seen[mid] < md5_item:
                low = mid + 1
            elif self.url_md5_seen[mid] >= md5_item:
                high = mid
        self.url_md5_seen.insert(low, md5_item)

    # 二分法查找url_md5存在于self.url_md5_set的位置，不存在返回-1
    def binary_md5_url_search(self, md5_item):
        low = 0
        high = len(self.url_md5_seen)
        if high == 0:
            return -1
        while (low < high):
            mid = (int)(low + (high - low) / 2)
            if self.url_md5_seen[mid] < md5_item:
                low = mid + 1
            elif self.url_md5_seen[mid] > md5_item:
                high = mid
            elif self.url_md5_seen[mid] == md5_item:
                return mid
        if low >= self.url_md5_seen.__len__():
            return -1
        if self.url_md5_seen[low] == md5_item:
            return low
        else:
            return -1