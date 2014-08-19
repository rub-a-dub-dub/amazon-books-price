# -*- coding: utf-8 -*-
import scrapy
import re
import json
from amazonCategories.items import AmazonBookPrices

class BookdetailsSpider(scrapy.Spider):
    name = "bookDetails"
    allowed_domains = ["amazon.com"]
    # start_urls = (
    #     'http://www.amazon.com/Saving-Animals-Earthquakes-Rescuing-Disasters/dp/1617722898/ref=sr_1_24?s=books&ie=UTF8&qid=1408248984&sr=1-24',
    # )

    def parse(self, response):
        # this will take us to the pricing page - not we just grab the first offer listing page, so hardcover, softcover et al are not going to be captured with this approach, a loop for all matching the xpath shown below will do the trick though, but additional logic will be needed to distinguish between the format based on the page contents

        try:
            pricePageLink = response.xpath('//a[contains(@href,"offer-listing")]/@href').extract()[0]
            try:
                itemID = re.search('\/gp\/offer-listing\/([0-9a-zA-Z]+)\/.*', pricePageLink).group(1)
                priceURL = 'http://www.amazon.com/gp/offer-listing/' + itemID + '/'
                yield scrapy.Request(priceURL, callback=self.pricelist, meta={'caller': response.url})
            except AttributeError:
                pass
        except IndexError:
            # not for sale!
            pass

    def pricelist(self, response):
        #  The loop below extracts all prices from this page
        for priceRow in response.xpath('//div[contains(@class,"olpOffer") and not(contains(@class, "a-container"))]'):
            priceItem = priceRow.xpath('div/span[contains(@class, "olpOfferPrice")]/text()').extract()
            shItem = priceRow.xpath('div/p/span/span[@class="olpShippingPrice"]/text()').extract()
            condItem = priceRow.xpath('div/h3/text()').extract()
            retVal = AmazonBookPrices()
            try:
                retVal["sh"] = shItem[0].strip()
            except:
                retVal["sh"] = ""
            retVal["cond"] = " ".join(condItem[0].strip().split())
            retVal["price"] = priceItem[0].strip()
            retVal["url"] = response.meta["caller"]
            yield retVal

        # This loop extracts price pagination links
        for pricePgLink in response.xpath('//ul[@class="a-pagination"]/li[not(@class)]/a/@href').extract():
            yield scrapy.Request("http://www.amazon.com" + pricePgLink, callback=self.pricelist, meta={'caller': response.meta["caller"]})

    def start_requests(self):
        # This grabs the list of URIs from /vagrant/books.json
        dataFile = "/vagrant/books.json"
        dataFid = open(dataFile)
        data = json.load(dataFid)
        
        # now loop through each item
        for item in data:
            url = item["url"]
            yield scrapy.Request(url, callback=self.parse)