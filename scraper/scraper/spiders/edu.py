# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class EduSpider(scrapy.Spider):
    name = "edu"
    allowed_domains = ["stanford.edu", "cmu.edu", "berkeley.edu", "mit.edu"]
    start_urls = (
        'http://www.stanford.edu/',
        'http://www.cmu.edu/',
        'http://www.berkeley.edu/',
        'http://web.mit.edu/'
    )

    def parse(self, response):
        links = response.xpath("//a/@href").extract()
        filename = "pages/" + response.url.replace("/", "|")
        open(filename, 'wb').write(response.body)
        for link in links:
            try:
                yield Request(link, callback=self.parse)
            except:
                pass

