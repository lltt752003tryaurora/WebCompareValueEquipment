# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import mysql.connector
import re
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class PriceValidatorPipeline:
    def process_item(self, item, spider):

        price = item.get('price')

        if price is not None:
            #price = re.sub("[^0-9\.]", "", price)
            tmp = re.findall('\d+', price)
            price = "".join(tmp)
    
            if price:
                # Convert to float
                price = float(price)

            else:
                price = None

        if price is not None :
            
            # Set normalised price
            item['price'] = price;

            return item
        else:
            raise DropItem(f"Missing price")

class MySQLPipeline:
    def __init__(self, mysql_host, mysql_user, mysql_pass, mysql_db):
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_pass = mysql_pass
        self.mysql_db = mysql_db
                
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host = crawler.settings.get('MYSQL_HOST'),
            mysql_user = crawler.settings.get('MYSQL_USER'),
            mysql_pass = crawler.settings.get('MYSQL_PASS'),
            mysql_db = crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self, spider):
        self.con = mysql.connector.connect(
            host = self.mysql_host,
            user = self.mysql_user,
            password = self.mysql_pass,
            database = self.mysql_db
        )

    def close_spider(self, spider):
        self.con.close()

    def process_item(self, item, spider):
        cursor = self.con.cursor()

        cursor.execute(
            'INSERT INTO products (url, price, title, img_url, shop_name) VALUES (%s, %s, %s, %s, %s)',
            (item['product_url'], item['price'], item['title'], item['img_url'], item['shop_name'])
        )

        self.con.commit()

        cursor.close();

        return item

class DuplicatesPipeline:
    def __init__(self):
        self.titles_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['title'] in self.titles_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.titles_seen.add(adapter['title'])
            return item