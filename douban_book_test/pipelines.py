# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DoubanBookTestPipeline:

    def __init__(self):
        self.__conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="123456",
            database="study",
            charset="utf8mb4"
        )
        self.__cur = self.__conn.cursor()

    def process_item(self, item, spider):
        sql = (
            f"insert into novel(book_name, book_img, pub_house, producer, pub_year, pages, bind, isbn, book_intro, author, author_profile, author_intro, douban_rating) "
            f"values ('{item['book_name']}', '{item['book_img']}', '{item['pub_house']}', '{item['producer']}','{item['pub_year']}','{item['pages']}','{item['bind']}','{item['isbn']}','{item['book_intro']}','{item['author']}','{item['author_profile']}','{item['author_intro']}','{item['douban_rating']}')")
        try:
            self.__cur.execute(
                sql)
            self.__conn.commit()
        except Exception:
            self.__conn.rollback()
        return item

    def close_spider(self, spider):
        self.__conn.close()
