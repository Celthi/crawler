import scrapy
import re
import urllib
import json
def authentication_failed(response):
    login_name_xpath = '//*[@id="wrapper_body"]/div/div/form/div/span/strong/text()'
    texts = response.xpath(login_name_xpath).getall()
    return "".join(texts).find("错误") != -1

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    visited_links = set('1') # the first page will always be crawled.
    config = {}
    def start_requests(self):
        urls = [
            'http://fund.sciencenet.cn/login',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            with open('./config.json') as f:
                self.config = json.load(f)
        except:
            self.logger.error('Please provide a ./config.json file!')
            raise Exception("No config.json file provided!")

        return scrapy.FormRequest.from_response(
            response,
            formdata={'phone': self.config["phone"], 'password': self.config["password"]},
            callback=self.after_login
        )

    def after_login(self, response):
        #TODO: the authentication check is never reached if the login is failed. The reason is when the login fails, after_login will never call which is due to scrapy duplicates filter.
        if authentication_failed(response):
            self.logger.error("Login failed")
            raise Exception("user name and password are not correct!")
        self.logger.info('Crawling for name = {}...'.format(self.config["name"]))
        return scrapy.Request(
            'http://fund.sciencenet.cn/search?name={name}&yearStart={yearStart}&yearEnd={yearEnd}&subject={subject}&category={category}&fundStart={fundStart}&fundEnd={fundEnd}&submit=list'.format(
                name = self.config["name"],
                yearStart = self.config['yearStart'],
                yearEnd = self.config['yearEnd'],
                subject = self.config['subject'],
                category = self.config['category'],
                fundStart = self.config['fundStart'],
                fundEnd = self.config['fundEnd']
            ),
            callback=self.after_search      
        )
    def iter_pages(self, response):
        def is_page_link(link):
            return re.search(urllib.parse.quote(self.name), link) != None
        pages_xpath = '//*[@id="page_button"]/span/a/@href'
        links = response.xpath(pages_xpath).getall()
        links = list(filter(is_page_link, links))
        return links

    def after_search(self, response):
        for item in self.collect_items(response):
            yield item
        for link in self.iter_pages(response):
            if not self.has_visited(link):
                self.visited_links.add(self.normalize(link))
                yield response.follow(link, callback = self.after_search)

    def normalize(self, link):
        pat = re.compile(r'page=(?P<page>\d{1,4})')
        m = pat.search(link)
        return m.group('page') if m else ''  
    def has_visited(self, link):
        normalize_link = self.normalize(link)
        return normalize_link in self.visited_links
    def collect_items(self, response):
        item_xpath = '//*[@id="resultLst"]/div[@class="item"]'
        for i in response.xpath(item_xpath):
            texts = i.xpath('p[@class="t"]/a//text()').getall()
            author = i.xpath('div[@class="d"]/p/span[1]/i/text()').get()
            number = i.xpath('div[@class="d"]/p/b/text()').get()
            research_type = i.xpath('div[@class="d"]/p/i/text()').get()
            department = i.xpath('div[@class="d"]/p/span[2]/i/text()').get()
            year = i.xpath('div[@class="d"]/p/span[3]/b/text()').get()
            money = i.xpath('div[@class="d"]/p[2]/span[1]/b/text()').get()
            keywords = i.xpath('div[@class="d"]/p[2]/span[2]/i/text()').getall()

            item = {
                "name": "".join(list(map(lambda s: s.strip(), texts))),
                "author": author,
                "number": number,
                "department": department,
                "research_type": research_type,
                "year": year,
                "money": money,
                "keywords": "".join(list(map(lambda s: s.strip(), keywords))),
                }
            yield item

