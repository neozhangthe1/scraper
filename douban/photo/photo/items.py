# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PhotoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    photo_id = scrapy.Field()
    movie_id = scrapy.Field()
    num_reply = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    type1 = scrapy.Field()
    type2 = scrapy.Field()
