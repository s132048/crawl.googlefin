# -*- coding: utf-8 -*-

from scrapy import Item, Field


class StockSymbolItem(Item):
    Exchange = Field()
    Company = Field()
    Symbol = Field()

class StockPriceItem(Item):
    Symbol = Field()
    Exchange = Field()
    Date = Field()
    Open = Field()
    Close = Field()
    High = Field()
    Low = Field()
    Volume = Field()
    Cdays = Field()
