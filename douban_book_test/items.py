# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class DoubanBookItem(scrapy.Item):
    # define the fields for your item here like:
    book_name = Field()
    book_img = Field()
    pub_house = Field()
    producer = Field()
    pub_year = Field()
    pages = Field()
    bind = Field()
    isbn = Field()
    book_intro = Field()
    author = Field()
    author_profile = Field()
    author_intro = Field()
    douban_rating = Field()
