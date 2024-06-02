import threading
from queue import Queue

import redis
import requests
from lxml import etree

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Cookie": 'bid=McvS1WhXwpM; _pk_id.100001.3ac3=b78b95d4902b9673.1717198454.; __utmc=30149280; __utmz=30149280.1717198454.1.1.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmc=81379588; __utmz=81379588.1717198454.1.1.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _vwo_uuid_v2=D93CC7778B9358D3134BF96E75DCEF268|f19a958d8512e501c35ca3cce7774def; push_noty_num=0; push_doumail_num=0; __utmv=30149280.28088; ct=y; viewed="4913064_36328704_35031587_34432750_20421947_36457094"; dbcl2="280881279:180b7JRfJpI"; ck=pu_0; ap_v=0,6.0; frodotk_db="066a8a71663e79ee133f9f5432bb6dca"; __utma=30149280.980919312.1717198454.1717234634.1717247773.5; __utmt_douban=1; __utmb=30149280.1.10.1717247773; __utma=81379588.900987245.1717198454.1717234634.1717247773.5; __utmt=1; __utmb=81379588.1.10.1717247773; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1717247773%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_ses.100001.3ac3=1'
}
item = {}
r = redis.Redis(
    host="127.0.0.1",
    port=6379,
    db=0
)

q2 = Queue()


def get_urls():
    tag_page = requests.get("https://book.douban.com/tag/?view=type&icn=index-sorttags-all", headers=header)
    if tag_page.status_code == 200:
        html = etree.HTML(tag_page.text)
        tags = html.xpath("//*//table[@class='tagCol']//tr//td//a/@href")
        http_urls = [f"https://book.douban.com{a}" for a in tags]
        url = http_urls[0]
        for i in range(50):
            urls = f"{url}?start={i * 20}&type=T"
            tag_get = requests.get(urls, headers=header)
            if tag_get.status_code == 200:
                html1 = etree.HTML(tag_get.text)
                a_href = html1.xpath("//*//ul[@class='subject-list']/li//a[@class='nbg']/@href")
                for pre_datas in a_href:
                    q2.put(pre_datas)


def push():
    while True:
        if q2.empty():
            break
        g = q2.get()
        print(f"pushing ---> {g}")
        r.lpush("books:start_urls", g)


if __name__ == '__main__':
    get_urls()
    t1_lst = []
    t2_lst = []
    for _ in range(8):
        t2 = threading.Thread(target=push)
        t2.start()
        t2_lst.append(t2)
    for i in t1_lst:
        i.join()
    for j in t2_lst:
        j.join()
