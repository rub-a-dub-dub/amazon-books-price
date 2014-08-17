# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AmazoncategoriesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = Field()
    url = scrapy.Field()
    name = scrapy.Field()
    count = scrapy.Field()
    ref = scrapy.Field()

class AmazonBookOverviewItem(scrapy.Item):
    # represents an Amazon book from the category listing page
    url = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()

class AmazonBookPrices(scrapy.Item):
    # Pricing details for a single item
    url = scrapy.Field()
    cond = scrapy.Field()
    price = scrapy.Field()
    sh = scrapy.Field()