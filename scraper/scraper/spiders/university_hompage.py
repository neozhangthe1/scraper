__author__ = 'yutao'

import scrapy
from scrapy.http import Request
from ..items import UniversityItem
import urlparse


class UniversityHompageSpider(scrapy.Spider):
    name = "university"

    allowed_domains = ["findaschool.org"]
    start_urls = (
        "http://www.findaschool.org/",
    )

    # def __init__(self):
    #     self.update_settings({
    #         "MONGODB_COLLECTION": "university"
    #     })

    def parse(self, response):
        if response.url == "http://www.findaschool.org/":
            links = response.xpath("//a[text()='Main']/@href").extract()
            for link in links:
                if not "//" in link:
                    link = urlparse.urljoin("http://www.findaschool.org/", link)
                try:
                    yield Request(link, callback=self.parse)
                except:
                    pass
        elif "?" in response.url:
            urls = response.xpath("//a/@href").extract()
            for link in urls:
                if not "//" in link:
                    link = urlparse.urljoin("http://www.findaschool.org/", link)
                try:
                    yield Request(link, callback=self.parse)
                except:
                    pass
            country = ""
            queries = response.url.split("?")[1].split("&")
            for q in queries:
                if "Country=" in q:
                    country = q.replace("Country=", "").replace("%20", " ")
                    break
            block = response.xpath("//ol[@class='normal']/li/a")
            for u in block:
                item = UniversityItem()
                item["url"] = u.xpath("@href").extract()[0]
                item["name"] = u.xpath("text()").extract()[0]
                item["_id"] = item["url"].replace("http://", "").replace("https://", "").replace("//", "").split("#")[0].strip("/")
                item["country"] = country
                yield item
