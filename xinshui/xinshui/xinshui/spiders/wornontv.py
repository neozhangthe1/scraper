# -*- coding: utf-8 -*-
import scrapy
import logging
from pymongo import MongoClient
import json
import codecs
from ..items import XinshuiItem

class WornontvSpider(scrapy.Spider):
    name = "wornontv"
    allowed_domains = ["wornontv.net"]

    def __init__(self):
        self.start_urls = []
        for t in range(20000, 30000):
            self.start_urls.append("http://wornontv.net/%s/" % t)
    # f_out = open("wornontv.txt", "w")

    # def parse(self, response):
    #     links = response.xpath("//div[@class='pure-g showlist']/div/ul/li/a")
    #     for link in links:
    #         url = link.xpath("@href").extract()[0]
    #         title = link.xpath("text()").extract()[0]
    #         # print url, title
    #         f_out.write(title + "|" + url + "\n")
    def parse(self, response):
        item = XinshuiItem()
        body = response.xpath("//div[@class='single-inner box']")
        img = body.xpath("//div['content-image']/p/img")
        breadcrumbs = body.xpath("//ul[@class='breadcrumbs']/li/a/span/text()").extract()
        item["_id"] = response.url.split("/")[-2]
        item['src'] = "tv"
        item['des'] = body.xpath("//div[@class='outfit-details-box']/h1/text()").extract()[0]
        item['show'] = breadcrumbs[1]
        item['episode'] = breadcrumbs[2]
        content_a = body.xpath("//span[@class='metabox-content pure-u-4-5']/a/text()").extract()
        content_t = body.xpath("//span[@class='metabox-content pure-u-4-5']/text()").extract()
        item['episode_name'] = content_a[0].strip()
        item['character'] = content_a[1].strip()
        item['actor'] = content_t[2].split("played by")[1].strip()
        item['post_time'] = content_t[3].strip()
        item['img'] = img.xpath("@src").extract()[0]
        if len(body.xpath("//div[@class='outfit-details-box']/p/text()").extract()) > 0:
            item["found"] = False
            yield item
        else:
            item["found"] = True
            item['brand'] = body.xpath("//span[@class='pure-u-4-5 outfit-details-content']/text()").extract()[0].split("by")[0].strip()
            item['product_type'] = body.xpath("//span[@class='pure-u-1-5 outfit-details-title']/strong/text()").extract()[0].split(":")[0].strip()
            products = body.xpath("//div[@class='product-item ']")
            match = []
            similar = []
            for p in products:
                product = {
                    "img": p.xpath("span/img/@src").extract()[0],
                    "url": p.xpath("a/@href").extract()[0],
                    "title": p.xpath("a/@title").extract()[0],
                    "price": p.xpath("a/span[@class='product-price']/text()").extract()[0],
                    "store": p.xpath("a/span[@class='product-store']/text()").extract()[0]
                }
                cat = p.xpath("a/img/@class").extract()[0]
                if cat == "exact-match":
                    match.append(product)
                else:
                    similar.append(product)
            item["match"] = match
            item["similar"] = similar
            yield item

