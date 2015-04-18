# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkedinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PersonProfileItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    photo = scrapy.Field()
    title = scrapy.Field()
    also_view = scrapy.Field()
    education = scrapy.Field()
    locality = scrapy.Field()
    industry = scrapy.Field()
    summary = scrapy.Field()
    specilities = scrapy.Field()
    skills = scrapy.Field()
    interests = scrapy.Field()
    group = scrapy.Field()
    honors = scrapy.Field()
    education = scrapy.Field()
    experience = scrapy.Field()
    overview_html = scrapy.Field()
    homepage = scrapy.Field()