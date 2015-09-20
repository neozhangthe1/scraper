
#encoding: utf-8
import re
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request

from ..items import PhotoItem

def gen_url(t, s, i):
    return "http://movie.douban.com/subject/" + i + "/photos?type=S&sortby=vote&size=a&subtype=" + t + "&start=" + s

class PhotoSpider(CrawlSpider):
    name = "photo"
    allowed_domains = ["movie.douban.com"]

    # rules = (
    #     Rule(LinkExtractor(allow=r"/subject/\d+/($|\?\w+)"),
    #         callback="parse"),
    # )

    # def __init__(self):
    start_urls = []
    ids = []
    f_in = open("ids.txt")
    for line in f_in:
        ids.append(line.strip())
    for i in ids:
        for t in ["o", "c", "w"]:
            start_urls.append(gen_url(t, "0", i))

    def parse(self, response):
        params = response.url.split("?")[1].split("&")
        mid = response.url.split("/")[4]
        data_dict = {}
        for p in params:
            x = p.split("=")
            data_dict[x[0]] = x[1]
        for link in response.xpath("//ul[@class='poster-col4 clearfix']/li"):
            tmp = link.xpath("@data-id").extract()
            if len(tmp) > 0:
                data_id = tmp[0]
            else:
                continue
            resolution = link.xpath("div[@class='prop']/text()").extract()[0].strip()
            width, height = resolution.split("x")

            item = PhotoItem()
            item["movie_id"] = mid
            item["photo_id"] = data_id
            item["width"] = int(width)
            item["height"] = int(height)
            item["type1"] = data_dict["type"]
            item["type2"] = data_dict["subtype"]

            yield item
        url = response.xpath("//span[@class='next']/a/@href").extract()
        if len(url) > 0:
            yield Request(url[0], callback=self.parse)


def get_all_id():
    from pymongo import MongoClient
    HOST = "127.0.0.1"
    PORT = 27017
    client = MongoClient(HOST, PORT)
    col = client.douban.movie
    ids = []
    for item in col.find():
        ids.append(item["subject_id"])
    f_out = open("ids.txt", "w")
    for i in ids:
        f_out.write(i + "\n")
    f_out.close()