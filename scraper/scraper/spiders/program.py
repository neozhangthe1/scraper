# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from tld import get_tld
from ..items import AdmissionPageItem
import logging
import urlparse

class ProgramSpider(scrapy.Spider):
    name = "program"
    #allowed_domains = ["stanford.edu", "cmu.edu", "berkeley.edu", "mit.edu"]
    start_urls = (
        "http://www.princeton.edu/",
        "http://www.stanford.edu",
        "http://www.cmu.edu/",
        "http://www.berkeley.edu/",
        "http://www.ucsd.edu/",
        "http://www.ucla.edu/"
        "http://www.mit.edu/",
        "http://www.harvard.edu/",
        "http://www.yale.edu/",
        "http://www.uiuc.edu/",
        "http://www.nyu.edu/",
        "http://www.brown.edu/",
        "http://www.byu.edu/"
        # "http://www.clas.ufl.edu/au/",
        # "http://univ.cc/search.php?dom=world&key=&start=1"
        # "http://univ.cc/search.php?dom=edu&key=&start=1"
    )

    def parse(self, response):
        title = response.xpath("//title/text()").extract()
        if len(title) > 0:
            title = title[0].strip()
        else:
            title = ""

        url = response.url
        domain = get_tld(url)
        urls = response.xpath("//a/@href").extract()
        links = []

        for link in urls:
            link = urlparse.urljoin(response.url, link)
            if not ".edu" in link:
                continue
            if ".txt" in link or ".pdf" in link:
                continue
            try:
                yield Request(link, callback=self.parse)
            except:
                pass

        if not "program" in title.lower() and not "program" in url.lower():
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
