# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .store import doubanDB

class PhotoPipeline(object):
    def process_item(self, item, spider):
        if spider.name != "photo":  return item
        if item.get("photo_id", None) is None: return item
        spec = { "photo_id": item["photo_id"] }
        doubanDB.photo.update(spec, {'$set': dict(item)}, upsert=True)

        return None