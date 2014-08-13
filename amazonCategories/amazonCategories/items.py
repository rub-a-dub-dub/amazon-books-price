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
