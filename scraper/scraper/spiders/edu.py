# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from tld import get_tld
from ..items import AdmissionPageItem
import logging

class EduSpider(scrapy.Spider):
    name = "edu"
    #allowed_domains = ["stanford.edu", "cmu.edu", "berkeley.edu", "mit.edu"]
    start_urls = (
        # 'http://www.stanford.edu/',
        # 'http://www.cmu.edu/',
        # 'http://www.berkeley.edu/',
        # 'http://web.mit.edu/',
        "http://www.clas.ufl.edu/au/",
        'http://admissions.colostate.edu/',
        'http://www.harvard.edu/admissions-aid',
        'http://admission.stanford.edu/',
        'http://admission.enrollment.cmu.edu/pages/engineering-programs-in-the-carnegie-institute-of-technology'
    )

    def parse(self, response):
        title = response.xpath("//title/text()").extract()
        if len(title) > 0:
            title = title[0]
        else:
            title = ""

        url = response.url
        domain = get_tld(url)
        urls = response.xpath("//a/@href").extract()
        links = []

        #filename = "pages/" + response.url.split("//")[1].strip("/").replace("/", "|")
        #open(filename, 'wb').write(response.body)
        for link in urls:
            if not ".edu" in link:
                continue
            if ".txt" in link or ".pdf" in link:
                continue
            try:
                yield Request(link, callback=self.parse)
            except:
                pass

        if not "admission" in title.lower() and not "admission" in url.lower():
            return

        item = AdmissionPageItem()

        logging.info("[Crawled]" + title)
        for anchor in response.xpath("//a"):
            t = anchor.xpath("text()").extract()
            u = anchor.xpath("@href").extract()
            if len(t) > 0:
                t = t[0]
            else:
                t = ""
            if len(u) > 0:
                u = u[0]
            else:
                u = ""
            links.append({
                "text": t,
                "url": u
            })

        item["_id"] = url.replace("http://", "").replace("https://", "").replace("//", "").split("#")[0].strip("/")
        item["title"] = title
        item["content"] = response.body
        item["domain"] = domain
        item["links"] = links
        item["url"] = url

        yield item
