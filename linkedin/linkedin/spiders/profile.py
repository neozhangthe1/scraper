__author__ = 'yutao'

from os import path
import os
import urllib

# from scrapy import Selector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
# from bs4 import UnicodeDammit

import random

import urllib, socket

from ..items import LinkedinItem, PersonProfileItem
from ..parsers.HtmlParser import HtmlParser
# from linkedin.db import MongoDBClient
import requests

CRAWL_NEIGHBOR = False

class LinkedinSpider(CrawlSpider):
    name = 'linkedin'
    allowed_domains = ['linkedin.com']

    start_urls = ["https://www.linkedin.com/in/feixia93"]

    rules = (
        # Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def __init__(self):
        # from pymongo import MongoClient
        # from ..settings import MONGODB_URI
        # db = MongoClient(MONGODB_URI)["bigsci"]
        # self.start_urls = []
        # cnt = 1
        # for item in db["linkedin"].find({}, {"url": 1}):
        #     if "pub-" in item["url"]:
        #         self.start_urls.append(item["url"])
        #     if cnt % 1000 == 0:
        #         print(cnt)
        #     cnt += 1
        #     if len(self.start_urls) > 10:
        #         break
        print(self.start_urls)
        self.proxies = []
        self.request20proxy = 'http://erwx.daili666.com/ip/?tid=558045424788230&num=100'
        self.request1proxy = 'http://erwx.daili666.com/ip/?tid=558045424788230&num=1'
        self.update_proxy()

    def update_proxy(self):
        proxy = urllib.urlopen(self.request20proxy)
        for line in proxy.readlines():
            print(line.strip())
            if "http" not in line.strip() and ":" in line.strip():
                self.proxies.append('http://' + line.strip())

    def choose_proxy(self):
        # print("num of proxies", len(self.proxies))
        while True:
            idx = random.randint(0, len(self.proxies) - 1)
            # print(idx)
            # print(self.proxies)
            p = self.proxies[idx]
            print(p)
            if not self.test_proxy(p):
                del self.proxies[idx]
                # proxy = urllib.urlopen(self.request1proxy)
                # for line in proxy.readlines():
                #     if not "http" in line.strip() and ":" in line.strip():
                #         p = 'http://' + line.strip()
                if len(self.proxies) < 20:
                    self.update_proxy()
            else:
                return p

    def test_proxy(self, proxy):
        # socket.setdefaulttimeout(3.0)
        test_url = 'http://www.linkedin.com'
        try:
            f = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=10)
        except requests.exceptions.ConnectTimeout:
            print("Proxy " + proxy + " fails!", "Timeout")
            return False
        except requests.exceptions.ConnectionError:
            print("Proxy " + proxy + " fails!", "ConnectionErr")
            return False
        except requests.exceptions.ReadTimeout:
            print("Proxy " + proxy + " fails!", "Read Timeout")
            return False
        # f = urllib.urlopen(test_url, proxies={'http': ':@' + proxy})
        # except TimeoutError:
        #     print("Proxy " + proxy + " fails!")
        #     return False
        else:
            if f.status_code != 200:
                print("Proxy " + proxy + " fails!", f.status_code)
                return False
            else:
                print("Proxy " + proxy + " is added.")
                return True

    def make_requests_from_url(self, url):
        request = Request(url, callback=self.parse)
        request.meta['proxy'] = self.choose_proxy()
        print("using proxy", request.meta['proxy'])
        request.headers['Proxy-Authorization'] = ''
        return request
    #

    def parse(self, response):
        """
        default parse method, rule is not useful now
        """
        response = response.replace(url=HtmlParser.remove_url_parameter(response.url))
        # hxs = HtmlXPathSelector(response)
        index_level = self.determine_level(response.url)
        if index_level in [1, 2, 3, 4]:
            # self.save_to_file_system(index_level, response)
            relative_urls = response.xpath("//a/@href").extract()#self.get_follow_links(index_level, response)
            if relative_urls is not None:
                for url in relative_urls:
                    request = Request(url, callback=self.parse)
                    request.headers['Proxy-Authorization'] = ''
                    request.meta['proxy'] = self.choose_proxy()
                    yield request
        elif index_level == 5:
            urls = response.xpath("//a/@href").extract()
            # print(urls)
            if CRAWL_NEIGHBOR:
                for link in urls:
                    if not self.determine_level(link) == 5:
                        continue
                    try:
                        request = Request(link, callback=self.parse)
                        # request.headers['Proxy-Authorization'] = ''
                        # request.meta['proxy'] = self.choose_proxy()
                        yield request
                        # yield Request(link, callback=self.parse)
                    except:
                        pass
            personProfile = HtmlParser.extract_person_profile(response)
            linkedin_id = self.get_linkedin_id(response.url)
            print("aa", linkedin_id)
            linkedin_id = urllib.unquote_plus(linkedin_id) #UnicodeDammit(urllib.unquote_plus(linkedin_id)).markup
            print("bb", linkedin_id)
            if linkedin_id:
                personProfile['_id'] = linkedin_id
                personProfile['url'] = response.url #UnicodeDammit(response.url).markup
                if "redirect_urls" in response.request.meta:
                    personProfile['redirect_urls'] = [HtmlParser.remove_url_parameter(u) for u in response.request.meta["redirect_urls"]]
                yield personProfile

    def determine_level(self, url):
        """
        determine the index level of current response, so we can decide wether to continue crawl or not.
        level 1: people/[a-z].htmlre
        level 2: people/[A-Z][\d+].html
        level 3: people/[a-zA-Z0-9-]+.html
        level 4: search page, pub/dir/.+
        level 5: profile page
        """
        import re

        if re.match(".+/[a-z]\.html", url):
            return 1
        elif re.match(".+/[A-Z]\d+.html", url):
            return 2
        elif re.match(".+/people-[a-zA-Z0-9-]", url):
            return 3
        elif re.match(".+/pub/dir/.+", url):
            return 4
        elif re.match(".+/search/._", url):
            return 4
        elif re.match(".+/pub/.+", url):
            return 5
        elif re.match(".+/in/.+", url):
            return 5
        return None

    def save_to_file_system(self, level, response):
        """
        save the response to related folder
        """
        if level in [1, 2, 3, 4, 5]:
            fileName = self.get_clean_file_name(level, response)
            if fileName is None:
                return

            fn = path.join(self.settings["DOWNLOAD_FILE_FOLDER"], str(level), fileName)
            self.create_path_if_not_exist(fn)
            if not path.exists(fn):
                with open(fn, "w") as f:
                    f.write(response.body)

    def get_clean_file_name(self, level, response):
        """
        generate unique linkedin id, now use the url
        """
        url = response.url
        if level in [1, 2, 3]:
            return url.split("/")[-1]

        linkedin_id = self.get_linkedin_id(url)
        if linkedin_id:
            return linkedin_id
        return None

    def get_linkedin_id(self, url):
        print(url)
        find_index = url.find("linkedin.com/")
        print(find_index)
        if find_index >= 0:
            return url[find_index + 13:].replace('/', '-')
        return None

    def get_follow_links(self, level, response):
        if level in [1, 2, 3]:
            relative_urls = response.xpath("//ul[@class='directory']/li/a/@href").extract()
            relative_urls = ["http://linkedin.com" + x for x in relative_urls]
            return relative_urls
        elif level == 4:
            relative_urls = relative_urls = response.xpath("//ol[@id='result-set']/li/h2/strong/a/@href").extract()
            relative_urls = ["http://linkedin.com" + x for x in relative_urls]
            return relative_urls

    def create_path_if_not_exist(self, filePath):
        if not path.exists(path.dirname(filePath)):
            os.makedirs(path.dirname(filePath))