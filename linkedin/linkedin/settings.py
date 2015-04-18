# -*- coding: utf-8 -*-

# Scrapy settings for linkedin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'linkedin'

SPIDER_MODULES = ['linkedin.spiders']
NEWSPIDER_MODULE = 'linkedin.spiders'

DOWNLOADER_MIDDLEWARES = {
    'linkedin.middleware.CustomHttpProxyMiddleware': 543,
    'linkedin.middleware.CustomUserAgentMiddleware': 545,
}


#DEPTH_PRIORITY = 1 #BFS
DEPTH_PRIORITY = 0 #DFS
#DEPTH_LIMIT = 4

ITEM_PIPELINES = [
  'scrapy_mongodb.MongoDBPipeline',
]

password = open("password.txt").next().strip()

MONGODB_URI = 'mongodb://yutao:%s@yutao.us:30017/bigsci' % password
MONGODB_DATABASE = 'bigsci'
# MONGODB_COLLECTION = 'university'
# MONGODB_COLLECTION = 'admission_pages'
MONGODB_COLLECTION = 'linkedin'
MONGODB_UNIQUE_KEY = '_id'
MONGODB_ADD_TIMESTAMP = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'linkedin (+http://www.yourdomain.com)'


# Enable auto throttle
AUTOTHROTTLE_ENABLED = True

COOKIES_ENABLED = False

# Set your own download folder
# DOWNLOAD_FILE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "download_file")