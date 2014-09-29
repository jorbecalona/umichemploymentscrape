# import requests
# import json
# from bs4 import BeautifulSoup

# from sets import Set
import scrapy
# from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from umichemploymentscrape.items import *
from scrapy import FormRequest
# import csv


class JobListingSpider(scrapy.Spider):
    name = "joblist"
    rootURL = "https://studentemployment.umich.edu/"
    rootStart = rootURL + "JobX_FindAJob.aspx?t=qs&qs=21"
    nextURLBase = rootURL + "JobX_FindAJob.aspx?s=1&ls=1&sdgpi="
    # rootURL = "https://studentemployment.umich.edu/JobX_FindAJob.aspx?s=1&ls=1&sdgpi=1"
    allowed_domains = ["umich.edu"]
    totalListings = 0
    totalListingsParsed = 0
    totalListPages = 0
    start_urls = ["https://studentemployment.umich.edu/JobX_ChooseFundingSources.aspx"]
    job_urls = []
    verbosemode = True
    # allScenes = Set()

    def parse(self, response):
        yield FormRequest.from_response(response,
            formname='aspnetForm',
            formdata={'Skin$body$FundingSourceChoices$0': '1', 'Skin$body$FundingSourceChoices$1': '0'},
            meta={'curr_listing_page': 1,  'flag': True},
            callback=self.after_login)

    def after_login(self, response):
        # yield Request(self.rootURL, callback=self.madeitmaybe)
        curr_listing_page = int(response.request.meta['curr_listing_page'])
        yield Request(
            self.rootStart,
            meta={'curr_listing_page': curr_listing_page, 'flag': True},
            callback=self.page_rs_50)

    def page_rs_50(self, response):
        self.totalListings = self.get_total_listings(response)
        print "Total Job Listings: %d" % self.totalListings
        self.totalListPages = (self.totalListings / 50) + 1 #for the url
        curr_listing_page = int(response.request.meta['curr_listing_page'])
        flag = response.request.meta['flag']
        self.job_urls.extend(self.get_job_links(response))
        # print self.job_urls

        # if curr_listing_page < self.totalListPages:
        if curr_listing_page < 1:
            curr_listing_page += 1
            nextPageURL = self.nextURLBase + str(curr_listing_page)
            print "NextPageURL: %s, CurrPage: %d" % (nextPageURL, curr_listing_page)
            yield Request(
                nextPageURL,
                meta={'curr_listing_page': curr_listing_page, 'flag': True},
                callback=self.page_rs_50
            )
        else:
            print "*********Done Collecting URLS***********"
            for INDEX, joburl in enumerate(self.job_urls):
                yield Request(self.rootURL + str(joburl), callback=self.parse_job)

    def madeitmaybe(self, response):
        self.totalListings = self.get_total_listings(response)
        print "Total Job Listings: %d" % self.totalListings
        thejoblinks = self.get_job_links(response)
        print thejoblinks
        # print "**********Made It Maybe******\n"
        yield self.totalListings

    def get_total_listings(self, response):
        pager = response.css('td.GraphicShell-Header1-Off span').xpath('text()').extract()
        return int(pager[-1].split(' ')[-1])

    def get_job_links(self, response):
        pageLinks = response.css('tr:nth-of-type(n+5) > td > a').xpath('@href').extract()
        return pageLinks

    def get_jobID(url):
        urls = str(url)
        ix1 = urls.find("JobID=") + 6
        ix2 = urls.find("&s")
        return urls[ix1:ix2]

    def parse_job(self, response):
        # JobFields = JobFields
        self.totalListingsParsed += 1
        print "\n********************Parsing Job: %d********************" % self.totalListingsParsed
        # R = response
        item = JobItem()
        raw_strs = response.css('table.RTG tr:nth-of-type(n+3) td:nth-of-type(2)')
        item[str(JobFields[0])] = self.getStr(response, response.css('td.GraphicShell-Header1-Off'))
        if verbosemode:
            print "[%s]: %s" % (str(JobFields[0]), self.getStr(response, response.css('td.GraphicShell-Header1-Off')))
        for index, elt in enumerate(raw_strs): # iteration over elts in table
             newField = self.getStr(response, elt)
             newFieldStr = str(' '.join(newField.split()))
             item[str(JobFields[int(index+1)])] = newFieldStr
             if verbosemode:
                print "[%s]: %s" % (JobFields[index+1], item[JobFields[index+1]])
        # item['_id'] = item['job_ID']
        return item

    def getStr(self, response, sel):
        raw_str_in = sel.xpath('text()').extract()[0].encode('utf-8')
        theoutstring = str(' '.join(raw_str_in.split()))
        if not theoutstring:
            return "N/A"
        else:
            return theoutstring
