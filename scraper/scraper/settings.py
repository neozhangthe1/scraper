# -*- coding: utf-8 -*-

# Scrapy settings for scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

#DEPTH_PRIORITY = 1 #BFS
DEPTH_PRIORITY = 0 #DFS
DEPTH_LIMIT = 5

ITEM_PIPELINES = [
  'scrapy_mongodb.MongoDBPipeline',
]

password = open("password.txt").next().strip()

MONGODB_URI = 'mongodb://yutao:%s@yutao.us:30017/bigsci' % password
MONGODB_DATABASE = 'bigsci'
# MONGODB_COLLECTION = 'university'
MONGODB_COLLECTION = 'admission_pages'
MONGODB_UNIQUE_KEY = 'url'
MONGODB_ADD_TIMESTAMP = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scraper (+http://www.yourdomain.com)'
