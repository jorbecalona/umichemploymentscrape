import requests
import json
from bs4 import BeautifulSoup

from sets import Set
import scrapy
# from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from umichemploymentscrape.items import *
from scrapy import FormRequest


class JobListingSpider(scrapy.Spider):
    name = "joblist"
    rootURL = "https://studentemployment.umich.edu/JobX_FindAJob.aspx?t=qs&qs=21"
    # rootURL = "https://studentemployment.umich.edu/JobX_FindAJob.aspx?s=1&ls=1&sdgpi=1"
    allowed_domains = ["umich.edu"]
    totalListings = 0
    # start_urls = [rootURL + "/brazzers-porn-directory/sites"]
    start_urls = ["https://studentemployment.umich.edu/JobX_ChooseFundingSources.aspx"]
    job_urls = []
    # allScenes = Set()

    def parse(self, response):
        yield FormRequest.from_response(response,
            formname='aspnetForm',
            formdata={'Skin$body$FundingSourceChoices$0': '1', 'Skin$body$FundingSourceChoices$1': '0'},
            meta={'curr_listing': 1, 'total_listings': 0, 'flag': True},
            callback=self.after_login)

    def after_login(self, response):
        yield Request(self.rootURL, callback=self.madeitmaybe)

    def page_rs_50(self, response):
        self.totalListings = self.get_total_listings(response)
        totalListPages = (self.totalListings / 50) + 1 #for the url
        curr = int(response.request.meta['curr_listing'])
        flag = response.request.meta['flag']
        response.css('tr:nth-of-type(n+5) > td > a')
        # self.job_urls.extend()


    def madeitmaybe(self, response):
        # print "\n**********Made It Maybe******"
        # print response.url
        # print "\n\n"
        # print response.body
        # totpages = response.css('td.GraphicShell-Header1-Off span').xpath('text()').extract()
        # for dod in totpages:
        #     print dod
        # # print "\n\n" + totpages
        # print "\n"
        # print totpages[-1].split(' ')[-1]
        self.totalListings = self.get_total_listings(response)
        print self.totalListings
        thejoblinks = get_job_links(response)
        # print "**********Made It Maybe******\n"
        yield self.totalListings

    def get_total_listings(self, response):
        pager = response.css('td.GraphicShell-Header1-Off span').xpath('text()').extract()
        return int(pager[-1].split(' ')[-1])

    def get_job_links(self, response):
        pageLinks = response.css('tr:nth-of-type(n+5) > td > a').xpath('@href').extract()
        if not pageLinks:
            print "empty pageLinks!!!!"
            return
        for link in pageLinks:
            print link
        return pageLinks

    # def parse(self, response):
    #     siteList = response.css('li.no-arrow-icon a')
    #     # print siteList
    #     for index, sel in enumerate(siteList):
    #         item = BrazzersSiteItem()
    #         item['title'] = str(sel.xpath('text()').extract()[0])
    #         item['link'] = str(self.rootURL + sel.xpath('@href').extract()[0])
    #         print "Parsing Site: %s, (%d of %d)" % (item['title'], index, len(siteList))
    #         yield Request(item['link'], callback=self.visitSitePage)
    #         # if index > 3:
    #         #     print "\n\n\nBreak!!!! Greater than 3 *********************\n\n\n"
    #         #     break

    # def visitSitePage(self, response):
    #     sceneList = response.css('div.release-card')
    #     for index, sel in enumerate(sceneList):
    #         yield self.getScene(response, sel)
    #     if self.getNext(response):
    #         yield Request(self.getNext(response), callback=self.visitSitePage)

    # def getScene(self, response, scene):
    #     item = BrazzersSceneItem()
    #     item['title'] = scene.css('h2.scene-card-title a').xpath('text()').extract()[0]
    #     item['title'] = str(' '.join(item['title'].split()))
    #     item['date'] = scene.css('time').xpath('text()').extract()[0]
    #     item['date'] = str(' '.join(item['date'].split()))
    #     item['link'] = self.rootURL + scene.css('h2.scene-card-title a').xpath('@href').extract()[0]
    #     item['site'] = str(scene.css('span.label-text').xpath('text()').extract()[0])
    #     item['siteAbv'] = str(scene.css('span.label-left-box').xpath('text()').extract()[0])
    #     item['filename'], item['corefilename'] = self.getVideoFileName(response, item['link'])
    #     # item['corefilename'] = self.getVideoFileName
    #     # item[''] = sel.css('div.model-names a').xpath('text()')
    #     # self.allScenes.add(item)
    #     self.sceneCount += 1
    #     print "Scene#: %d - %s - %s - %s" % (self.sceneCount, item['siteAbv'], item['corefilename'], item['date'])
    #     return item

    # def getVideoFileName(self, response, videoURL):
    #     r = requests.get(videoURL)
    #     soup = BeautifulSoup(r.content)
    #     soupstring = str(soup.prettify('latin-1'))
    #     scrStart = soupstring.find("var videoUiInfoObject") + 24
    #     scrEnd = soupstring.find("var isiPad") - 6
    #     data = json.loads(soupstring[scrStart:scrEnd])
    #     videoStreamURL = data['player']['stream_info']['http']['paths'].values()[0]
    #     video_Fname = videoStreamURL.split('/')[5].split('?')[0]
    #     videoFileNameList = video_Fname.split('_')[:4] + video_Fname.split('_')[-2:]
    #     videoFileName = ('_'.join(map(str, videoFileNameList)))
    #     videoCoreFileName = ('_'.join(map(str, videoFileNameList[:4]))) + str(videoFileNameList[-1][-4:])
    #     return (videoFileName, videoCoreFileName)

    # def getNext(self, response):
    #     nextLink = response.css('li.paginationui-nav.next a').xpath('@href').extract()
    #     if nextLink:
    #         return self.rootURL + nextLink[0]
    #     else:
    #         return False
