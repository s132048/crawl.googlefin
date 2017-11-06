# -*- coding: utf-8 -*-

from scrapy import Item, Field


class StockSymbolItem(Item):
    symbol = Field()
    exchange_symbol = Field()
    name = Field()

class InactiveSymbolItem(Item):
    symbol = Field()
    exchange_symbol = Field()

class StockExchangeItem(Item):
    exchange_symbol = Field()
    country = Field()
    name = Field()

class StockPriceItem(Item):
    name = Field()
    exchange_symbol = Field()
    date = Field()
    open = Field()
    close = Field()
    high = Field()
    low = Field()
    volume = Field()
    cdays = Field()
