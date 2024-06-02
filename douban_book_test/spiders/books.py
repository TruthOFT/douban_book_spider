import scrapy
from scrapy.http import HtmlResponse, Request
from scrapy import Selector
from douban_book_test.items import DoubanBookItem
import re
from scrapy_redis.spiders import RedisSpider


class BookSpider(RedisSpider):
    name = "books"
    # allowed_domains = ["book.douban.com"]
    # start_urls = ["https://book.douban.com/tag/?view=type&icn=index-sorttags-all"]
    redis_key = "books:start_urls"

    def parse(self, response: HtmlResponse, **kwargs):
        item = DoubanBookItem()
        book_name = response.xpath("//div[@id='wrapper']//h1/span/text()").extract()
        book_img = response.xpath("//div[@id='mainpic']//a[@class='nbg']/@href").extract()
        pub_house = response.xpath(
            "//div[@id='info']/span[@class='pl' and contains(text(), '出版社')]/following-sibling::a[1]/text()").extract()
        producer = response.xpath(
            "//div[@id='info']/span[@class='pl'][contains(text(),'出品方')]/following-sibling::a[1]/text()").extract()
        pub_year = response.xpath(
            "//div[@id='info']/span[@class='pl'][contains(text(),'出版年')]/following-sibling::text()[1]").extract()
        pages = response.xpath(
            "//div[@id='info']/span[@class='pl' and contains(text(), '页数')]/following-sibling::text()[1]").extract()
        bind = response.xpath(
            "//div[@id='info']/span[@class='pl' and contains(text(), '装帧')]/following-sibling::text()[1]").extract()
        isbn = response.xpath(
            "//div[@id='info']/span[@class='pl' and contains(text(), 'ISBN')]/following-sibling::text()[1]").extract()
        book_intro = response.xpath("//*//div[@id='link-report']//p/text()").extract()
        author = response.xpath(
            "//div[@id='info']//span[@class='pl' and contains(text(), '作者')]/following-sibling::a[1]/text()").extract()
        author_profile = response.xpath("//div[@id='authors']//li[@class='author']//img/@src").extract()
        author_intro = response.xpath(
            "//*//h2//span[contains(text(),'作者简介')]/../following-sibling::*//div[@class='intro']//p/text()").extract()
        rating = response.xpath("//*//div[@id='interest_sectl']//strong/text()").extract()
        if len(book_name) > 0:
            item["book_name"] = book_name[0]
        else:
            item["book_name"] = ""
        if len(book_img) > 0:
            item["book_img"] = book_img[0]
        else:
            item["book_img"] = ""
        if len(pub_house) > 0:
            item["pub_house"] = pub_house[0]
        else:
            pub_house = response.xpath("//span[text()='出版社:']/following-sibling::text()[1]")
            if len(pub_house) > 0:
                item["pub_house"] = pub_house[0]
            else:
                item["pub_house"] = ""
        if len(producer) > 0:
            item["producer"] = producer[0]
        else:
            item['producer'] = ""
        item["pub_year"] = pub_year[0].strip()
        if len(pages) > 0:
            item["pages"] = pages[0].strip()
        else:
            item["pages"] = ""
        if len(bind) > 0:
            item["bind"] = bind[0].strip()
        else:
            item["bind"] = ""
        if len(isbn) > 0:
            item["isbn"] = isbn[0].strip()
        else:
            item["isbn"] = ""
        item["book_intro"] = "".join(book_intro)
        if len(author) > 0:
            item["author"] = author[0]
        else:
            item["author"] = ""
        if len(author_profile) > 0:
            item["author_profile"] = author_profile[0]
        else:
            item["author_profile"] = ""
        if len(author_intro) > 0:
            item["author_intro"] = "".join(author_intro)
        else:
            item["author_intro"] = ""
        item["douban_rating"] = rating[0].strip()
        yield item
        # sel = Selector(response)
        # a_href = sel.xpath("//*//ul[@class='subject-list']/li//a[@class='nbg']/@href").extract()
        # pre_book_name = sel.xpath("//div[@class='info']/h2/a/text()").extract()
        # book_names_lst = []
        # for i in pre_book_name:
        #     book_name = re.sub(r"\s+", "", i.replace("\n", ""))
        #     if book_name != "" or book_name != '':
        #         book_names_lst.append(book_name)
        # name_and_href = dict(zip(book_names_lst, a_href))
        # print(name_and_href, len(name_and_href))
        # # for a in a_href:
        # #     print(f"---tag--- {a}")
        # #     yield Request(url=a, callback=self.__parse_detail, cb_kwargs={'item': item})
        # for name, href in name_and_href.items():
        #     item = DoubanBookItem()
        #     item['book_name'] = name
        #     yield Request(url=href, callback=self.__parse_detail, cb_kwargs={'item': item},
        #                   meta={'dont_redirect': True, 'handle_httpstatus_list': [302]}, dont_filter=True)

    # def __parse_tag(self, response: HtmlResponse):
    #     sel = Selector(response)
    #     a_href = sel.xpath("//*//ul[@class='subject-list']/li//a[@class='nbg']/@href").extract()
    #     pre_book_name = sel.xpath("//div[@class='info']/h2/a/text()").extract()
    #     book_names_lst = []
    #     for i in pre_book_name:
    #         book_name = re.sub(r"\s+", "", i.replace("\n", ""))
    #         if book_name != "" or book_name != '':
    #             book_names_lst.append(book_name)
    #     name_and_href = dict(zip(book_names_lst, a_href))
    #     print(name_and_href, len(name_and_href))
    #     # for a in a_href:
    #     #     print(f"---tag--- {a}")
    #     #     yield Request(url=a, callback=self.__parse_detail, cb_kwargs={'item': item})
    #     for name, href in name_and_href.items():
    #         item = DoubanBookItem()
    #         item['book_name'] = name
    #         yield Request(url=href, callback=self.__parse_detail, cb_kwargs={'item': item},
    #                       meta={'dont_redirect': True, 'handle_httpstatus_list': [302]}, dont_filter=True)

    def __parse_detail(self, response: HtmlResponse, **kwargs):
        item = kwargs['item']
