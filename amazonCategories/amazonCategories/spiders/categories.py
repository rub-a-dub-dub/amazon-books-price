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
        for category in response.xpath('//div[@class="categoryRefinementsSection"]/ul[2]/li[a/span[@class="refinementLink"]]'):
            retItem = AmazoncategoriesItem()
            twoVals = category.xpath('a/span/text()').extract()
            retItem['name'] = twoVals[0]
            retItem['count'] = twoVals[1]
            retItem['url'] = response.url
            retItem['ref'] = response.request.headers.get('Referer', None)
            searchURL = category.xpath('a/@href').extract()
            yield retItem
            yield scrapy.Request(searchURL[0], callback=self.parse)
