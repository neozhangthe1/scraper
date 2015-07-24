# -*- coding: utf-8 -*-
import scrapy
import logging
from pymongo import MongoClient
import json
import codecs
from ..items import ThetakeItem
from scrapy.http import Request

class WornontvSpider(scrapy.Spider):
    name = "thetake"
    allowed_domains = ["thetake.com"]

    def __init__(self):
        self.start_urls = []
        # self.start_urls = ["https://thetake.com/product/85815/daniel-craig-npeal-spectre-cable-roll-neck-cashmere-sweater-spectre"]
        for id in reversed(range(97123)):
            self.start_urls.append("https://thetake.com/product/" + str(id) + "/")
    # f_out = open("wornontv.txt", "w")

    # def parse(self, response):
    #     links = response.xpath("//div[@class='pure-g showlist']/div/ul/li/a")
    #     for link in links:

    #         url = link.xpath("@href").extract()[0]
    #         title = link.xpath("text()").extract()[0]
    #         # print url, title
    #         f_out.write(title + "|" + url + "\n")
    def parse(self, response):
        item = ThetakeItem()
        img = response.xpath("//img[@id='productCropImage']/@src").extract()
        item["_id"] = response.url.split("/")[-2]
        item['src'] = "movie"
        if len(img) > 0:
            item['img'] = img[0]
        else:
            print("no img")
        tmp = response.xpath("//a[@id='actorName']/text()").extract()
        if len(tmp) > 0:
            item['actor'] = tmp[0]
        else:
            print('no actor')
        tmp = response.xpath("//a[@id='actorName']/@href").extract()
        if len(tmp) > 0:
            item['actor_url'] = tmp[0]
        else:
            print('no actor_url')
        tmp = response.xpath("//a[@id='movieName']/text()").extract()
        if len(tmp) > 0:
            item['movie'] = tmp[0]
        else:
            print('no movie')
        tmp = response.xpath("//a[@id='movieName']/@href").extract()
        if len(tmp) > 0:
            item['movie_url'] = tmp[0]
        else:
            print('no movie url')
        tmp = response.xpath("//strong[@class='pro-details-description-header']/text()").extract()
        if len(tmp) > 0:
            item['des_header'] = [0]
        else:
            print("no des header")
        item['des'] = "".join(response.xpath("//div[@class='pro-details-description']/text()").extract()).strip()
        item['category'] = response.xpath("//a[@class='pro-detail-cat']/text()").extract()
        #
        # relative_urls = response.xpath("//a/@href").extract()#self.get_follow_links(index_level, response)
        # if relative_urls is not None:
        #     for url in relative_urls:
        #         if "/product/" in url:
        #             yield Request("http://thetake.com" + url, callback=self.parse)

        exact = False
        product_img = ""
        productBrand = ""
        productName = ""
        if len(response.xpath("//div[@class='circle exact-match']")) > 0:
            exact = True
        tmp = response.xpath("//img[@id='productImage']/@src").extract()
        if len(tmp) > 0:
            product_img = tmp[0]
        else:
            print("no product_img")
        tmp = response.xpath("//h2[@id='productBrand']/text()").extract()
        if len(tmp) > 0:
            productBrand = tmp[0]
        else:
            print("no brand")
        tmp = response.xpath("//h1[@id='productName']/text()").extract()
        if len(tmp) > 0:
            productName = tmp[0]
        else:
            print("no name")
        priceCurrency = response.xpath("//div[@id='productPriceTest']/meta[@itemprop='priceCurrency']/@content").extract()
        price = response.xpath("//div[@id='productPriceTest']/meta[@itemprop='priceCurrency']/@content").extract()
        url = response.xpath("//div[@id='productPriceTest']/meta[@itemprop='priceCurrency']/@content").extract()
        p = {
            "match": exact,
            "img": product_img,
            "brand": productBrand,
            "name": productName
        }
        if len(priceCurrency) > 0:
            p["currency"] = priceCurrency[0],
        if len(price) > 0:
            p["price"] = price[0],
        if len(url) > 0:
            p["store"] = url[0]

        sss = []
        similar = response.xpath("//ul[@id='similarList']/li")
        for s in similar:
            xx = s.xpath("div[@class='similar-thumb']/div/img/@alt").extract()[0].split("-")
            ss = {
                "img": s.xpath("div[@class='similar-thumb']/div/img/@src").extract()[0],
                "brand": xx[0].strip(),
                "name": xx[1].strip(),
                "price": s.xpath("div[@class='similar-price']/a/text()").extract()[0].strip(),
                "store": s.xpath("div[@class='similar-price']/a/@href").extract()[0].strip(),
                "id": s.xpath("div[@class='similar-price']/a/@data-id").extract()[0].strip()
            }
            sss.append(ss)
        item["match"] = p
        item["similar"] = sss
        yield item