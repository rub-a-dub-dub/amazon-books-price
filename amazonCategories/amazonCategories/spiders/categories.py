# -*- coding: utf-8 -*-
import scrapy
from amazonCategories.items import AmazoncategoriesItem

class CategoriesSpider(scrapy.Spider):
    name = "categories"
    allowed_domains = ["amazon.com"]
    start_urls = (
        'http://www.amazon.com/books-used-books-textbooks/b/ref=topnav_storetab_b?ie=UTF8&node=283155',
    )

    def parse(self, response):
        namePrefix = ''
        # get parent names
        for name in response.xpath('//div[@class="categoryRefinementsSection"]/ul[last()]/li[@class="shoppingEngineExpand"]/a/span[2]/text()'):
            namePrefix = namePrefix + "." + name.extract()

        # get current item name
        name = response.xpath('//div[@class="categoryRefinementsSection"]/ul[last()]/li/strong/text()')
        if len(name) > 0:
            name = name[0]
            namePrefix = namePrefix + "." + name.extract()

        # get rid of the prefixed "."
        if len(namePrefix) > 0:
            namePrefix = namePrefix[1:]

        # now process the links on this page
        for category in response.xpath('//div[@class="categoryRefinementsSection"]/ul[last()]/li[a/span[@class="refinementLink"]]'):
            retItem = AmazoncategoriesItem()
            twoVals = category.xpath('a/span/text()').extract()
            searchURL = category.xpath('a/@href').extract()
            retItem['name'] = namePrefix + "." + twoVals[0]
            retItem['count'] = twoVals[1]
            retItem['url'] = searchURL[0]
            retItem['ref'] = response.url
            #retItem['ref'] = response.request.headers.get('Referer', None)
            yield retItem
            yield scrapy.Request(searchURL[0], callback=self.parse)
