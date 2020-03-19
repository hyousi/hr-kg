# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaidubkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    birth = scrapy.Field()

    def __str__(self):
        return f'{self["birth"]}-{self["name"]}'


class RelationItem(scrapy.Item):
    subj = scrapy.Field()
    pred = scrapy.Field()
    obj = scrapy.Field()

    def __str__(self):
        return f"{self['subj']}-{self['pred']}-{self['obj']}"
