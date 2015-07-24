# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThetakeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    img = scrapy.Field()
    _id = scrapy.Field()
    src = scrapy.Field()
    actor = scrapy.Field()
    actor_url = scrapy.Field()
    movie = scrapy.Field()
    movie_url = scrapy.Field()
    des_header = scrapy.Field()
    des = scrapy.Field()
    category = scrapy.Field()
    match = scrapy.Field()
    similar = scrapy.Field()
