# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XinshuiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    src = scrapy.Field()
    des = scrapy.Field()
    show = scrapy.Field()
    episode = scrapy.Field()
    episode_name = scrapy.Field()
    character = scrapy.Field()
    actor = scrapy.Field()
    post_time = scrapy.Field()
    brand = scrapy.Field()
    product_type = scrapy.Field()
    img = scrapy.Field()
    match = scrapy.Field()
    similar = scrapy.Field()
    found = scrapy.Field()

