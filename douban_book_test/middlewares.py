# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import random
import time

from fake_useragent import UserAgent
from scrapy import signals, Request

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


def get_cookie():
    cookie_str = 'bid=McvS1WhXwpM; _pk_id.100001.3ac3=b78b95d4902b9673.1717198454.; __utmc=30149280; __utmz=30149280.1717198454.1.1.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmc=81379588; __utmz=81379588.1717198454.1.1.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _vwo_uuid_v2=D93CC7778B9358D3134BF96E75DCEF268|f19a958d8512e501c35ca3cce7774def; push_noty_num=0; push_doumail_num=0; __utmv=30149280.28088; ct=y; viewed="4913064_36328704_35031587_34432750_20421947_36457094"; dbcl2="280881279:180b7JRfJpI"; ck=pu_0; ap_v=0,6.0; frodotk_db="066a8a71663e79ee133f9f5432bb6dca"; __utma=30149280.980919312.1717198454.1717234634.1717247773.5; __utmt_douban=1; __utmb=30149280.1.10.1717247773; __utma=81379588.900987245.1717198454.1717234634.1717247773.5; __utmt=1; __utmb=81379588.1.10.1717247773; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1717247773%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_ses.100001.3ac3=1'
    cookies_dict = {}
    for item in cookie_str.split("; "):
        k, v = item.split("=", maxsplit=1)
        cookies_dict[k] = v
    return cookies_dict


class DoubanBookTestSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class DoubanBookTestDownloaderMiddleware:

    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # headers = random.choice(spider.settings['USER_AGENT_LIST'])
        # request.headers['User-Agent'] = headers
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class RandomDelayMiddleware(object):
    def __init__(self, delay_a, delay_b):
        self.delay_a = delay_a
        self.delay_b = delay_b

    @classmethod
    def from_crawler(cls, crawler):
        delay_a = crawler.spider.settings.get("RANDOM_DELAY_A", 3)
        delay_b = crawler.spider.settings.get("RANDOM_DELAY_B", 5)
        if not isinstance(delay_a, int):
            raise ValueError("RANDOM_DELAY need a int")
        return cls(delay_a, delay_b)

    def process_request(self, request, spider):
        # delay = random.randint(0, self.delay)
        delay = random.uniform(self.delay_a, self.delay_b)
        delay = float("%.1f" % delay)
        logging.debug("### random delay: %s s ###" % delay)
        time.sleep(delay)


COOKIES = get_cookie()


class RandomUserAgentListMiddleware(UserAgentMiddleware):
    """
        自动随机更换UA
    """

    def __init__(self, user_agent_list):
        super(RandomUserAgentListMiddleware, self).__init__()
        self.user_agent_list = user_agent_list

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent_list=crawler.settings.get('USER_AGENT_LIST')
        )

    def process_request(self, request, spider):
        random_user_agent = random.choice(self.user_agent_list)
        logging.info(f"### user-agent {random_user_agent} ###")
        request.headers.setdefault('User-Agent', random_user_agent)


class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()

        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request: Request, spider):
        def get_ua():
            # print(request.headers)
            return getattr(self.ua, self.ua_type)

        request.cookies = COOKIES
        agent = get_ua()
        logging.debug(f"### agent {agent}")
        request.headers.setdefault('User-Agent', agent)
