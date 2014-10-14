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
import textwrap
# import csv


class JobListingSpider(scrapy.Spider):
    name = "joblist"
    rootURL = "https://studentemployment.umich.edu/"
    rootStart = rootURL + "JobX_FindAJob.aspx?t=qs&qs=21"
    nextURLBase = rootURL + "JobX_FindAJob.aspx?s=1&ls=1&sdgpi="
    # rootURL = "https://studentemployment.umich.edu/Job
    # X_FindAJob.aspx?s=1&ls=1&sdgpi=1"
    allowed_domains = ["umich.edu"]
    totalListings = 0
    totalListingsParsed = 0
    totalListPages = 0
    start_urls = [
        "https://studentemployment.umich.edu/JobX_ChooseFundingSources.aspx"]
    job_urls = [rootStart]
    verbosemode = False
    verboseSeeData = True
    dbName = 'umichscrape'
    jsonFileName = 'jobs.json'
    navLinks = []

    # allScenes = Set()

    def parse(self, response):
        yield FormRequest.from_response(
            response,
            formname='aspnetForm',
            formdata={'Skin$body$FundingSourceChoices$0': '1',
                      'Skin$body$FundingSourceChoices$1': '0'},
            meta={'curr_listing_page': 1,  'flag': False},
            callback=self.after_login)

    def after_login(self, response):
        # yield Request(self.rootURL, callback=self.madeitmaybe)
        curr_listing_page = int(response.request.meta['curr_listing_page'])
        yield Request(
            self.rootStart,
            meta={'curr_listing_page': curr_listing_page, 'flag': False},
            callback=self.page_rs_50)

    def page_rs_50(self, response):
        flag = response.request.meta['flag']
        if not flag:
            self.totalListings = self.get_total_listings(response)
            print "Total Job Listings: %d" % self.totalListings
        self.totalListPages = (self.totalListings / 50) + 1  # for the url
        # curr_listing_page = int(response.request.meta['curr_listing_page'])
        # curJobLinks = self.get_job_links(response)
        # self.job_urls.extend(curJobLinks)
        # print self.job_urls
        # if curr_listing_page < 1:
        print 'Extending navLinks'
        self.navLinks.extend(
            [self.navPage(i) for i in range(2, self.totalListPages)])
        print 'Begin Iteration over navLinks'
        # for I, S in enumerate(self.navLinks):
        for I, S in enumerate(self.navLinks[:1]):
            if self.verbosemode:
                print 'Request for Nav Page#: {}'.format(I)
            yield Request(
                S,
                meta={'curr_listing_page': I, 'flag': True},
                callback=self.getJobsFromNavPage
                )
        # if curr_listing_page < self.totalListPages:
        #     print "Current Listing Page#: %d" % (curr_listing_page)
        #     curr_listing_page += 1
        #     nextPageURL = self.nextURLBase + str(curr_listing_page)
        #     # if not verbosemode:
        #     # print "NextPageURL: %s, CurrPage: %d" % (
        #         # nextPageURL, curr_listing_page)
        #     yield Request(
        #         nextPageURL,
        #         meta={'curr_listing_page': curr_listing_page, 'flag': True},
        #         callback=self.page_rs_50
        #     )
        # else:
        #     # if not verbosemode:
        #     print "*********Done Collecting URLS***********"
        #     for INDEX, joburl in enumerate(self.job_urls):
        #         yield Request(self.rootURL + str(joburl),
        #                       callback=self.parse_job)

    def navPage(self, num):
        nPage =  self.nextURLBase + str(num)
        if self.verbosemode:
            print 'navPage: {}'.format(nPage)
        return nPage

    def jobPage(self, suffix):
        jPage = self.rootURL + str(suffix)
        if self.verbosemode:
            print 'jPage: {}'.format(jPage)
        return jPage

    def getJobsFromNavPage(self, response):
        # print 'inside getJobsFromNavPage now'
        curr_listing_page = int(response.request.meta['curr_listing_page'])
        if self.verbosemode:
            print '----Call to ~getJobsFromNavPage: {}'.format(curr_listing_page)
        # curJobLinks = self.get_job_links(response)
        curJobLinks = self.getFullJobLinks(response)
        if self.verbosemode:
            print 'Extending job_urls'
        self.job_urls.extend(curJobLinks)
        # print curJobLinks
        for index, s in enumerate(curJobLinks):
            if self.verbosemode:
                print '----|----Call to ~parse_job on index: {}'.format(index)
            yield Request(s, callback=self.parse_job)

    def madeitmaybe(self, response):
        self.totalListings = self.get_total_listings(response)
        print "Total Job Listings: %d" % self.totalListings
        thejoblinks = self.get_job_links(response)
        print thejoblinks
        # print "**********Made It Maybe******\n"
        yield self.totalListings

    def get_total_listings(self, response):
        pager = response.css(
            'td.GraphicShell-Header1-Off span').xpath('text()').extract()
        return int(pager[-1].split(' ')[-1])

    def get_job_links(self, response):
        pageLinks = response.css(
            'tr:nth-of-type(n+5) > td > a').xpath('@href').extract()
        return pageLinks

    def getFullJobLinks(self, response):
        # pL = self.get_job_links(response)
        pageLinks = response.css(
            'tr:nth-of-type(n+5) > td > a').xpath('@href').extract()
        pL = [self.jobPage(link) for link in pageLinks]
        return pL

    def get_jobID(url):
        urls = str(url)
        ix1 = urls.find("JobID=") + 6
        ix2 = urls.find("&s")
        return urls[ix1:ix2]

    def parse_job(self, response):
        # JobFields = JobFields
        self.totalListingsParsed += 1
        # print "Parsing Job: %d" % self.totalListingsParsed
        # R = response
        item = JobItem()
        raw_strs = response.css(
            'table.RTG tr:nth-of-type(n+3) td:nth-of-type(2)')
        item[str(JobFields[0])] = self.getStr(
            response,
            response.css('td.GraphicShell-Header1-Off'))
        # if not verbosemode:
        # print "[%s]: %s" % (str(JobFields[0]),
            # self.getStr(response, response.css(
                # 'td.GraphicShell-Header1-Off')))
        # if self.verbosemode or self.verboseSeeData:
        strHead = 'Parsing Job: {}'.format(self.totalListingsParsed)
        strHeadForm = '<{0:-^82}>'.format(strHead)
        # print '\n\t<-- Parsing Job: {} --> '.format(self.totalListingsParsed)
        print '\n{}'.format(strHeadForm)
        for index, elt in enumerate(raw_strs):
            # iteration over elts in table
            newField = self.getStr(response, elt)
            newFieldStr = str(' '.join(newField.split()))
            item[str(JobFields[int(index+1)])] = newFieldStr
            if self.verbosemode or self.verboseSeeData:
                pstring = str('{0:<27}| {1:>50}'.format(
                    str(' [{}]:'.format(JobFields[index+1])),
                    self.getPropStr(response, item[JobFields[index+1]])
                    # str(item[JobFields[index+1]])[:50]
                    )
                )
                    # JobFields[index+1],
                    # item[JobFields[index+1]]
                    # textwrap.fill(
                    #     str(item[JobFields[index+1]]),
                    #     width=50,
                    #     initial_indent='',
                    #     subsequent_indent='\t\t\t    | ')
                    # align=80
                    # align=(76-len(JobFields[index+1])-20)
                # print 'pstring: {}'.format(pstring)
                # propList = (textwrap.wrap(pstring, width=80))[0]
                dtext = textwrap.dedent(pstring) #.strip()
                dtextwrap = textwrap.wrap(
                                dtext, width=80,
                                initial_indent='',
                                subsequent_indent='\t\t\t    | ')
                for ind, wl in enumerate(dtextwrap[:2]):
                    pass
                    # print '{:->}'.format(wl)

                print pstring
                # print textwrap.fill(dtext, width=80)
                # print self.getPropStr(response, pstring)
                # print pstring
                # print ' -->[{}]: {}'.format(
                #     JobFields[index+1],
                #     item[JobFields[index+1]])
        # item['_id'] = item['job_ID']
        return item

    def getPropStr(self, response, strin):
        # propStr = (textwrap.wrap(strin, width=77))[0]
        propStr = strin[:50]
        propStr = propStr.strip()
        # Gets the first line
        if len(strin) > 50:
            propStr += ' (...)'
        return str(propStr)

    def getStr(self, response, sel):
        raw_str_in = sel.xpath('text()').extract()[0].encode('utf-8')
        theoutstring = str(' '.join(raw_str_in.split()))
        if not theoutstring:
            return "N/A"
        else:
            return theoutstring
