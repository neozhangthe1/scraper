__author__ = 'yutao'

# -*- coding: utf-8 -*-
import scrapy
import logging
from pymongo import MongoClient
import json
import codecs
from ..items import ThetakeItem
from scrapy.http import Request

class TheTakeSpider(scrapy.Spider):
    name = "actor"
    allowed_domains = ["thetake.com"]

    def __init__(self):
        self.start_urls = []
        # self.start_urls = ["https://thetake.com/product/85815/daniel-craig-npeal-spectre-cable-roll-neck-cashmere-sweater-spectre"]
        id = 23700
        while id < 100000:
            self.start_urls.append("https://thetake.com/actors/listActors?limit=100&start=" + str(id))
            id += 100

    def parse(self, response):
        js_resp = json.loads(response.body_as_unicode())

        for d in js_resp:
            item = ThetakeItem()
            item["_id"] = "actor/" + str(d["id"])
            item["data_type"] = "actor"
            item["data"] = d
            yield item