import scrapy
import csv
import datetime
from ..items import StockPriceItem, StockSymbolItem
from dateutil.parser import parse
import pandas as pd
from scrapy.loader import ItemLoader

class PriceSpider(scrapy.Spider):
    name = 'getprices'

    def start_requests(self):
        SymbolLoader = ItemLoader(item=StockSymbolItem())
        Symbols = SymbolLoader.get_value('Code')
        for i in Symbols[:10]:
            yield scrapy.Request('https://finance.google.com/finance/getprices?q=%s&p=40Y&f=d,c,v,k,o,h,l' %i)

    def parse(self, response):
        SPI = StockPriceItem()
        page = response.text

        sdate = self.startdate
        edate = self.enddate


        list_contents = []
        series_contents = pd.Series()
        a = csv.StringIO(page)
        b = csv.reader(a)

        for i in b:

            if len(i) == 7:
                list_contents.append(i)

        list_contents = list_contents[1:]

        for i in list_contents:

            if len(i[0]) > 4:
                stamp = int(i[0][1:])
                date = datetime.datetime.fromtimestamp(stamp).date()
                i[0] = str(date)
                series_contents[i[0]] = i[1:]

            else:
                i[0] = str(date + datetime.timedelta(int(i[0])))
                series_contents[i[0]] = i[1:]

        for i in range(100):
            datecheck = str(parse(sdate).date() + datetime.timedelta(i))
            if datecheck in series_contents.keys():
                sdate = datecheck
                break

        for i in range(100):
            datecheck = str(parse(edate).date() - datetime.timedelta(i))
            if datecheck in series_contents.keys():
                edate = datecheck
                break

        output = series_contents[sdate:edate].to_dict()



        yield output

