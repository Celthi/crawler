import scrapy
import re
import urllib
import json


class QuotesSpider(scrapy.Spider):
    name = "bianzhi"
    visited_links = set('1')  # the first page will always be crawled.
    config = {}
    count = 0

    def start_requests(self):
        urls = [
            'http://www.shiyebian.net/zhejiang/hangzhou/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            with open('./config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except:
            self.logger.error('Please provide a ./config.json file!')
            raise Exception("No config.json file provided!")
        for item in self.collect_items(response):
            yield item
        for link in self.iter_pages(response):
            if not self.has_visited(link):
                self.count += 1
                if self.count > 20:
                    break
                self.visited_links.add(link)
                yield response.follow(link, callback=self.parse)

    def iter_pages(self, response):
        pages_xpath = "//div[contains(@class, 'listlie')]/ul/li/a/@href"
        links = response.xpath(pages_xpath).getall()
        return links


    def has_visited(self, link):
        return link in self.visited_links

    def collect_items(self, response):
        item_xpath = '//a[contains(text(), "附件") and substring(@href, string-length(@href) - 3) = ".xls"]'
        for i in response.xpath(item_xpath):
            yield self.get_item(i)

    def get_item(self, item):
        url = item.xpath('@href').get()
        name = item.xpath('text()').get()

        return {
            "name": "".join(map(lambda s: s.strip(), name)),
            "url": url
        }
