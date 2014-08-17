# -*- coding: utf-8 -*-
import scrapy
import json
import random
from amazonCategories.items import AmazonBookOverviewItem

class BooklistcategorySpider(scrapy.Spider):
    name = "bookListCategory"
    allowed_domains = ["amazon.com"]
    # need to sample at least these many percent and # items
    minThreshPct = 15.0
    minThreshVal = 20
    # this is the maximum number of pages Amazon makes available
    maxPages = 100
    # this is the number of items/page
    itemsPerPage = 12

    def parse(self, response):
        # We'll be given a page here and will have to return
        # all (up to 12) book items
        pgCat = response.xpath('//h2[@id="s-result-count"]/a/text()').extract()
        pgCat = ".".join(pgCat)

        for result in response.xpath('//div[starts-with(@id, "result_")]'):
            baseLink = result.xpath('/div[@class="data"]/h3/a')
            url = baseLink.xpath('/@href').extract()[0]
            name = baseLink.xpath('/text()').extract()[0]
            retVal = AmazonBookOverviewItem()
            retVal['url'] = url
            retVal['name'] = name
            retVal['category'] = pgCat
            yield retVal

    def start_requests(self):
        # load up our URLs from the prior processing step
        dataFile = "/vagrant/leafcats.json"
        dataFid = open(dataFile)
        data = json.load(dataFid)
        
        # now loop through each item
        for item in data:
            numItems = item["count"]
            url = item["url"]
            # this is the number of items we're going to be reading
            scanItems = max(numItems*self.minThreshPct/100, self.minThreshVal)
            # this is the number of pages we'll be requesting
            scanPages = int(scanItems/self.maxPages)
            if scanPages > self.maxPages: scanPages = self.maxPages
            # randomly sample pages we need from the range amazon allows
            pages = random.sample(xrange(1, self.maxPages), scanPages)
            # now generate page URLs for each randomly sampled page number
            for pg in pages:
                crawlURL = url + "&page=" + str(pg)
                yield scrapy.Request(crawlURL, callback=self.parse)