import scrapy
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from tech_scraper.items import Product

class GearVNCrawlSpider(CrawlSpider):
    name = 'gearvn_cspider'
    allowed_domains = ["gearvn.com"]
    start_urls = [
        "https://gearvn.com",
        #"https://gearvn.com/pages/laptop-van-phong",
        #"https://gearvn.com/collections/vo-case-custom-water-cooling/?page=1",
    ]

    rules = (
        Rule(
            LinkExtractor(allow=('/pages/', )),
            follow = True,  
        ),

        Rule(
            LinkExtractor(allow=('/collections/',)),
            callback = 'parse',  
            follow = True,
        ),

        # # Extract links matching 'category.php' (but not matching 'subsection.php')
        # # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=('//', ))),

        # # Extract links matching 'item.php' and parse them with the spider's method parse_item
        # Rule(LinkExtractor(allow=('item\.php', )), callback='parse'),
    )

    def parse(self, response):
        products = Selector(response).css('div.col-sm-4')
        for product in products:
            item = Product()
            item['title'] = product.css('h2.product-row-name').xpath('text()').extract()[0]
            item['price'] = product.css('span.product-row-sale').xpath('text()').extract()[0]
            item['product_url'] = 'https://gearvn.com' + product.css('a.product-row-btnbuy').attrib['href']
            item['img_url'] = product.css('img.product-row-thumbnail').attrib['src']
            item['shop_name'] = 'GearVN'
            yield item

    # def parse(self, response):
    #     item = Product()
    #     item['title'] = response.css('h1.product_name').xpath('text()').extract()[0].strip()
    #     item['price'] = response.css('td.variant-control').attrib['data-price']
    #     item['product_url'] = response.request.url
    #     item['img_url'] = response.css('div.fotorama').xpath('img/@src').extract()[0]
    #     item['shop_name'] = 'GearVN'
    #     return item

# class GearVNSpider(Spider):
#     name = 'gearvn_spider'
#     allowed_domains = ["gearvn.com"]
#     start_urls = [
#         #"https://gearvn.com",
#         #"https://gearvn.com/pages/laptop-van-phong",
#         "https://gearvn.com/collections/vo-case-custom-water-cooling/?page=1",
#     ]

#     def parse(self, response):
#         products = Selector(response).css('div.col-sm-4')
#         for product in products:
#             item = Product()
#             item['title'] = product.css('h2.product-row-name').xpath('text()').extract()[0]
#             item['price'] = product.css('span.product-row-sale').xpath('text()').extract()[0]
#             item['product_url'] = 'https://gearvn.com' + product.css('a.product-row-btnbuy').attrib['href']
#             item['img_url'] = product.css('img.product-row-thumbnail').attrib['src']
#             item['shop_name'] = 'GearVN'
#             yield item

#     # def parse(self, response):
#     #     item = Product()
#     #     item['title'] = response.css('h1.product_name').xpath('text()').extract()[0].strip()
#     #     item['price'] = response.css('td.variant-control').attrib['data-price']
#     #     item['product_url'] = response.request.url
#     #     item['img_url'] = response.css('div.fotorama').xpath('img/@src').extract()[0]
#     #     item['shop_name'] = 'GearVN'
#     #     return item