# -*- coding: utf-8 -*-

from scrapy import Item, Field


class StockSymbolItem(Item):
    symbol = Field()
    exchange_symbol = Field()
    name = Field()

class StockExchangeItem(Item):
    exchange_symbol = Field()
    country = Field()
    name = Field()

class StockDailyPriceItem(Item):
    symbol = Field()
    exchange_symbol = Field()
    date = Field()
    open = Field()
    close = Field()
    high = Field()
    low = Field()
    volume = Field()