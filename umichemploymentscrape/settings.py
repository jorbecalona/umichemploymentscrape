# -*- coding: utf-8 -*-

# Scrapy settings for umichemploymentscrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'umichemploymentscrape'

SPIDER_MODULES = ['umichemploymentscrape.spiders']
NEWSPIDER_MODULE = 'umichemploymentscrape.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'umichemploymentscrape (+http://www.yourdomain.com)'
USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36"

LOG_FILE='scrape.log'

ITEM_PIPELINES = {
    'umichemploymentscrape.pipelines.UmichemploymentscrapePipeline': 2
    # 'umichemploymentscrape.pipelines.couchdbPipeline': 1
}

