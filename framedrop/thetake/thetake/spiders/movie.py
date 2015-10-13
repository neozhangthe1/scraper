# -*- coding: utf-8 -*-
import scrapy
import logging
from pymongo import MongoClient
import json
import codecs
from ..items import ThetakeItem
from scrapy.http import Request

class TheTakeSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["thetake.com"]

    def __init__(self):
        self.start_urls = []
        # self.start_urls = ["https://thetake.com/product/85815/daniel-craig-npeal-spectre-cable-roll-neck-cashmere-sweater-spectre"]
        id = 0
        while id < 10000:
            self.start_urls.append("https://thetake.com/movies/listMovies?limit=100&start=" + str(id))
            id += 100

    def parse(self, response):
        js_resp = json.loads(response.body_as_unicode())

        for d in js_resp:
            item = ThetakeItem()
            item["_id"] = "movie/" + str(d["id"])
            item["data_type"] = "movie"
            item["data"] = d
            yield item