# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import oss2
import pymysql
import requests
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
        self.__auth = oss2.Auth(self.__ACCESS_KEY, self.__ACCESS_KEY_SECRET)
        self.__bucket = oss2.Bucket(self.__auth, self.__endpoint, self.__BUCKET_NAME)

    def __put_data(self, data):
        c = data.rfind("/")
        obj_name = data[c + 1::]
        inp_data = requests.get(data)
        self.__bucket.put_object(obj_name, inp_data)
        self.__bucket.put_object_acl(obj_name, oss2.OBJECT_ACL_PUBLIC_READ)
        return f"https://{self.__bucket}.{self.__endpoint}/{obj_name}"

    def process_item(self, item, spider):
        author_profile = item["author_profile"]
        print(author_profile)
        book_img = item["book_img"]
        author_url = self.__put_data(author_profile)
        cover_url = self.__put_data(book_img)
        sql = f"insert into authors(name, photo, biography) values ('{item['author']}', '{author_url}', '{item['author_intro']}')"
        try:
            self.__cur.execute(sql)
            author_id = self.__conn.insert_id()
            sql2 = (
                f"insert into books(title, cover_image, publisher, producer, publish_date, pages, binding, isbn, description,douban_rating) values ("
                f"'{item['book_name']}', '{cover_url}', '{item['pub_house']}', '{item['producer']}', '{item['pub_year']}', '{item['pages']}', '{item['bind']}', '{item['isbn']}', '{item['book_intro']}', '{item['douban_rating']}')")
            self.__cur.execute(sql2)
            book_id = self.__conn.insert_id()
            sql3 = f"insert into bookauthors(book_id, author_id) values ('{book_id}', '{author_id}')"
            self.__cur.execute(sql3)
            self.__conn.commit()
        except pymysql.MySQLError:
            self.__conn.rollback()
        return item

    def close_spider(self, spider):
        self.__conn.close()
