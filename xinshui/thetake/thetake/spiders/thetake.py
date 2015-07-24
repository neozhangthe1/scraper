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
        item['actor'] = response.xpath("//a[@id='actorName']/text()").extract()[0]
        item['actor_url'] = response.xpath("//a[@id='actorName']/@href").extract()[0]
        item['movie'] = response.xpath("//a[@id='movieName']/text()").extract()[0]
        item['movie_url'] = response.xpath("//a[@id='movieName']/@href").extract()[0]
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
        if len(response.xpath("//div[@class='circle exact-match']")) > 0:
            exact = True
        product_img = response.xpath("//img[@id='productImage']/@src").extract()[0]
        productBrand = response.xpath("//h2[@id='productBrand']/text()").extract()[0]
        productName = response.xpath("//h1[@id='productName']/text()").extract()[0]
        priceCurrency = response.xpath("//div[@id='productPriceTest']/meta[@itemprop='priceCurrency']/@content").extract()[0]
        price = response.xpath("//div[@id='productPriceTest']/meta[@itemprop='priceCurrency']/@content").extract()[0]
        url = response.xpath("//div[@id='productPriceTest']/meta[@itemprop='priceCurrency']/@content").extract()[0]
        p = {
            "match": exact,
            "img": product_img,
            "brand": productBrand,
            "name": productName,
            "currency": priceCurrency,
            "price": price,
            "store": url
        }
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