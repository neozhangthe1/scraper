# -*- coding: utf-8 -*-
import scrapy
import logging

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
        self.start_urls = []
        self.url_to_id = {}
        client = MongoClient('mongodb://yutao:911106zyt@yutao.us:30017/bigsci')
        db = client["bigsci"]
        col = db["people"]
        data = col.find({"contact.homepage":{"$exists":True}}, timeout=False)
        for item in data:
            hp = item["contact"]["homepage"]
            self.start_urls.append(hp)
            self.url_to_id[hp] = item["_id"]
        print len(self.start_urls), "urls"


    def parse(self, response):
        if response.url in self.url_to_id:
            f_out = codecs.open(self.url_to_id[response.url] + ".html", "w", encoding="utf-8")
            f_out.write(response.text)
            f_out.close()