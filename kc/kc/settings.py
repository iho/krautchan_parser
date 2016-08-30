# -*- coding: utf-8 -*-

# Scrapy settings for kc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'kc'

SPIDER_MODULES = ['kc.spiders']
NEWSPIDER_MODULE = 'kc.spiders'

CONCURRENT_REQUESTS = 3
DOWNLOAD_DELAY = 0.250 

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'kc (+http://www.yourdomain.com)'
