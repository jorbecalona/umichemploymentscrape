# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import couchdb
from umichemploymentscrape.dataManage import *

class UmichemploymentscrapePipeline(object):
    def process_item(self, item, spider):
        return item

class JsonPipeline(object):
    def __init__(self):
        self.file = open('jobsNew.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class couchdbPipeline(object):
    def __init__(self):
        self.server = couchdb.Server()
        self.db = self.server['umichscrape']
        self.file = open('jobs.json', 'wb')

    def process_item(self, item, spider):
        item['_id'] = item['job_ID']
        self.db.save(dict(item))
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
