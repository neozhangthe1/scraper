#encoding: utf-8
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request

from pymongo import MongoClient
db = MongoClient("yutao.yt:11060")["botify"]
col = db["subject"]

class YouzySpider(CrawlSpider):
    name = 'youzy'
    allowed_domains = ['youzy.cn']
    start_urls = ['http://www.youzy.cn/major/index']


    def parse_discipline(self, response):
        majors = []

        major_list = response.xpath("//div[@class='major-list-con']")
        for major_elem in major_list:
            m1 = {
                "name": major_elem.xpath("h1/text()").extract()[0],
                "children": []
            }
            major_2_list = major_elem.xpath("h2/text()").extract()
            major_3_elems = major_elem.xpath("ul")
            for i, major_3_elem in enumerate(major_3_elems):
                m2 = {
                    "name": major_2_list[i],
                    "children": []
                }
                for major_3_item in major_3_elem.xpath("li"):
                    m3 = {
                        "name": major_3_item.xpath("a/text()").extract()[0],
                        "des": major_3_item.xpath("a/@data-content").extract()[0],
                        "url": "http://www.youzy.cn/" + major_3_item.xpath("a/@href").extract()[0]
                    }
                    m2["children"].append(m3)
                m1["children"].append(m2)

            majors.append(m1)
        import json
        import codecs
        with codecs.open("学科.json", "w", "utf-8") as f_out:
            json.dump(majors, f_out, ensure_ascii=False, indent=2)

    def get_urls(self, response):
        urls = response.xpath("//div[@class='major-list-con']/ul/li/a/@href").extract()
        urls = ["http://www.youzy.cn" + u.replace("explain", "OpenCollege") for u in urls]
        return urls


    def parse(self, response):
        """
        Scrapy creates scrapy.http.Request objects for each URL in the
        start_urls attribute of the Spider, and assigns them the parse method
        of the spider as their callback function.
        """
        print(response.url)
        if 'index' in response.url:
            urls = self.get_urls(response)
            for u in urls:
                yield Request(u, callback=self.parse)

        elif "opencollege" in response.url.lower():
            print(response.url)
            for elem in response.xpath("//ul[@class='uzy-college-list']/li"):
                d = {
                    "subject": response.xpath("//div[@class='major-right']/div[@class='major-info']/h3/text()").extract()[0].strip(),
                    "subject_info": response.xpath("//div[@class='major-right']/div[@class='major-info']/div[@class='info']/span/text()").extract()[0],
                    "name": elem.xpath("div/div[@class='top']/a/text()").extract()[0],
                    "name_en": elem.xpath("div[@class='mark']/a/img/@alt").extract()[0],
                    "img": elem.xpath("div[@class='mark']/a/img/@src").extract()[0],
                    "url":  "http://www.youzy.cn" + elem.xpath("div/div[@class='top']/a/@href").extract()[0],
                    "tags": elem.xpath("div/div/div[@class='tag']/img/@title").extract(),
                    "properties": elem.xpath("div/div[@class='bottom']/ul/li/text()").extract(),
                    "art": False
                }
                if len(elem.xpath("div/div[@class='bottom']/img")) > 0:
                    d["art"] = True
                col.insert(d)

                cur_page = 0
                tmp = response.url.split("page=")
                if len(tmp) > 1:
                    cur_page = int(tmp[1])
                else:
                    tmp[0] += "?"

                pagination = response.xpath("//ul[@class='pagination']/li/a/text()").extract()
                if len(pagination) > 0:
                    try:
                        last_page = int(pagination[-1])
                    except:
                        last_page = int(pagination[-2])
                    if last_page != cur_page:
                        yield Request(tmp[0] + "page=" + str(cur_page + 1), callback=self.parse)

