# -*- coding: utf-8 -*-

from scrapy import Item, Field


class StockSymbolItem(Item):
    Exchange = Field()
    Company = Field()
    Symbol = Field()
    AWS_RDS_URI = Field()

