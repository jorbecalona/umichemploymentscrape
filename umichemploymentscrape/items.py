# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class JobListingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = scrapy.Field()
    job_url = scrapy.Field()
    date_posted = scrapy.Field()
    employer = scrapy.Field()
    category = scrapy.Field()

class JobItem(scrapy.Item):
    job_title = scrapy.Field()
    job_ID = scrapy.Field()
    job_funding_source = scrapy.Field()
    employer = scrapy.Field()
    category = scrapy.Field()
    job_description = scrapy.Field()
    educational_value = scrapy.Field()
    job_requirements = scrapy.Field()
    hours = scrapy.Field()
    compensation = scrapy.Field()
    when_job_is_avaliable = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    contact_person = scrapy.Field()
    contact_email = scrapy.Field()
    supervisor = scrapy.Field()
    work_location = scrapy.Field()
    phone_number = scrapy.Field()
    fax_number = scrapy.Field()

JobFields = [
    'job_title', 'job_ID', 'job_funding_source', 'employer', 'category',
    'job_description', 'educational_value', 'job_requirements',
    'hours', 'compensation', 'when_job_is_avaliable', 'start_date',
    'end_date', 'contact_person', 'contact_email', 'supervisor',
    'work_location', 'phone_number', 'fax_number']