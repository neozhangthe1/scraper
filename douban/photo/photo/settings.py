# -*- coding: utf-8 -*-

# Scrapy settings for photo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'photo'

SPIDER_MODULES = ['photo.spiders']
NEWSPIDER_MODULE = 'photo.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'photo (+http://www.yourdomain.com)'
ITEM_PIPELINES = {
    "photo.pipelines.PhotoPipeline": 1,
}

DOWNLOADER_MIDDLEWARES = {
    "photo.misc.middlewares.CustomUserAgentMiddleware": 401,
    "photo.misc.middlewares.CustomCookieMiddleware": 701,
    "photo.misc.middlewares.CustomHeadersMiddleware": 551,
}

