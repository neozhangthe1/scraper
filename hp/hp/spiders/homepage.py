# -*- coding: utf-8 -*-
import scrapy
import logging
from pymongo import MongoClient
import json
import codecs

class HPSpider(scrapy.Spider):
    name = "hp"
    #allowed_domains = ["stanford.edu", "cmu.edu", "berkeley.edu", "mit.edu"]
    # start_urls = (
    #     # 'http://www.stanford.edu/',
    #     # 'http://www.cmu.edu/',
    #     # 'http://www.berkeley.edu/',
    #     # 'http://web.mit.edu/',
    #     "http://www.clas.ufl.edu/au/",
    #     'http://admissions.colostate.edu/',
    #     'http://www.harvard.edu/admissions-aid',
    #     'http://admission.stanford.edu/',
    #     'http://admission.enrollment.cmu.edu/pages/engineering-programs-in-the-carnegie-institute-of-technology'
    # )
    def __init__(self):
        self.url_to_id = json.load(codecs.open("url.json"))
        del self.url_to_id[""]
        self.start_urls = self.url_to_id.keys()
        print len(self.start_urls), "urls"


    def parse(self, response):
        if response.url in self.url_to_id:
            f_out = codecs.open(self.url_to_id[response.url] + ".html", "w", encoding="utf-8")
            f_out.write(response.text)
            f_out.close()