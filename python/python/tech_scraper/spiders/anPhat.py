import scrapy
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from tech_scraper.items import Product
from w3lib.url import url_query_cleaner

# def process_links(links):
#     for link in links:
#         link.url = url_query_cleaner(link.url)
#         yield link

class AnPhatCrawlSpider(CrawlSpider):
    name = 'anphat_cspider'
    allowed_domains = ["anphatpc.com.vn"]
    start_urls = [
        "https://www.anphatpc.com.vn",
        #"https://gearvn.com/pages/laptop-van-phong",
    ]

    rules = (
        Rule(
            LinkExtractor(allow=('.html', ), deny=('filter=','sort=','min=','max=','brand=')),
            #process_links=process_links,
            callback = 'parse',
            follow = True,  
        ),

        # Rule(
        #     LinkExtractor(allow=('/collections/',)),
        #     callback = 'parse',  
        # ),
    )

    def parse(self, response):
        products = Selector(response).css('div.js-p-item')
        for product in products:
            item = Product()
            item['title'] = product.css('a.p-name').xpath('h3/text()').extract()[0]
            item['price'] = product.css('span.p-price').xpath('text()').extract()[0]
            item['product_url'] = 'https://www.anphatpc.com.vn/' + product.xpath('a/@href').extract()[0]
            item['img_url'] = product.xpath('a/img/@data-src').extract()[0]
            item['shop_name'] = 'An Phát Computer'
            yield item

# class AnPhatSpider(Spider):
#     name = 'anphat_spider'
#     allowed_domains = ["anphatpc.com.vn/"]
#     start_urls = [
#         "https://www.anphatpc.com.vn/may-tinh-xach-tay-laptop.html",
#         #"https://gearvn.com/pages/laptop-van-phong",
#     ]

#     def parse(self, response):
#         products = Selector(response).css('div.js-p-item')
#         for product in products:
#             item = Product()
#             item['title'] = product.css('a.p-name').xpath('h3/text()').extract()[0]
#             item['price'] = product.css('span.p-price').xpath('text()').extract()[0]
#             item['product_url'] = 'https://www.anphatpc.com.vn/' + product.xpath('a/@href').extract()[0]
#             item['img_url'] = product.xpath('a/img/@data-src').extract()[0]
#             item['shop_name'] = 'An Phát Computer'
#             yield item