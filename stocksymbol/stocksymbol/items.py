# -*- coding: utf-8 -*-

from scrapy import Item, Field


class StockSymbolItem(Item):
    country = Field()
    exchange = Field()
    company = Field()
    symbol = Field()
    AWS_RDS_URI = Field()

