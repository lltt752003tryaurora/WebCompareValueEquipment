import scrapy
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from tech_scraper.items import Product

class PhongVuCrawlSpider(CrawlSpider):
    name = 'phongvu_cspider'
    allowed_domains = ["phongvu.vn"]
    start_urls = [
        # "https://phongvu.vn",
        "https://phongvu.vn/c/laptop",
        "https://phongvu.vn/c/san-pham-apple",
        "https://phongvu.vn/c/do-gia-dung-thiet-bi-gia-dinh",
        "https://phongvu.vn/c/pc",
        "https://phongvu.vn/c/man-hinh-may-tinh",
        "https://phongvu.vn/c/linh-kien-may-tinh",
        "https://phongvu.vn/c/phu-kien-pc",
        "https://phongvu.vn/c/hi-end-gaming",
        "https://phongvu.vn/c/dien-thoai-may-tinh-bang-phu-kien",
        "https://phongvu.vn/c/phu-kien-chung",
        "https://phongvu.vn/c/thiet-bi-am-thanh",
        "https://phongvu.vn/c/thiet-bi-thong-minh",
        "https://phongvu.vn/c/thiet-bi-van-phong",
        "https://phongvu.vn/c/giai-phap-doanh-nghiep",
    ]

    rules = (
        Rule(
            LinkExtractor(allow=('/c/', )),
            callback = 'parse',  
            follow =  True,
        ),
    )

    def parse(self, response):
        products = Selector(response).xpath('//a[@class="css-pxdb0j"]')
        for product in products:
            item = Product()
            item['title'] = product.xpath('div/div[3]/div/h3/text()').extract()[0]
            item['price'] = product.xpath('div/div[4]/div/div/text()').extract()[0]
            item['product_url'] = "https://phongvu.vn" + product.xpath('@href').extract()[0]
            item['img_url'] = product.xpath('div/div/div/div/img/@src').extract()[0]
            item['shop_name'] = 'Phong Vũ'
            yield item
