# -*- coding: utf-8 -*-
import scrapy
import logging
from pymongo import MongoClient
import json
import codecs
from ..items import ThetakeItem
from scrapy.http import Request

class TheTakeSpider(scrapy.Spider):
    name = "thetake"
    allowed_domains = ["thetake.com"]

    def __init__(self):
        self.start_urls = []
        # self.start_urls = ["https://thetake.com/product/85815/daniel-craig-npeal-spectre-cable-roll-neck-cashmere-sweater-spectre"]
        # for id in reversed(range(97123)):
        #     self.start_urls.append("https://thetake.com/products/danielRelated?limit=100&start=&productId=%s" % str(id))
        id = 0
        while id < 100000:
            self.start_urls.append("https://thetake.com/products/listProducts?limit=25&start=" + str(id))
            id += 25

    def parse(self, response):
        js_resp = json.loads(response.body_as_unicode())

        for d in js_resp:
            item = ThetakeItem()
            item["_id"] = d["id"]
            item["data_type"] = "product"
            item["data"] = d
            yield item