import scrapy
import csv
import datetime
import pandas as pd
from ..items import StockPriceItem
from dateutil.parser import parse

class PriceSpider(scrapy.Spider):
    name = 'getprices'

    def start_requests(self):

        symbols = pd.read_csv('../symbols/symbols.csv')
        if self.code in symbols.Symbol.values:
            symbols = symbols[symbols.Symbol == self.code]
        if self.ex in symbols.Exchange.values:
            symbols = symbols[symbols.Exchange == self.ex]
        S = parse(self.startdate).date()
        duration = datetime.datetime.now().date() - S
        D = duration.days//365 + 1

        for i in range(len(symbols)):
            symbol = symbols.Symbol[i]
            exchange = symbols.Exchange[i]
            yield scrapy.Request('https://finance.google.com/finance/getprices?q=%s&x=%s&p=%sY&f=d,c,v,k,o,h,l' %(symbol, exchange, D))

    def parse(self, response):
        page = response.text
        S = parse(self.startdate).date()
        E = parse(self.enddate).date()


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

        for i in range(300):
            datecheck = str(S + datetime.timedelta(i))
            if datecheck in series_contents.keys():
                startdate = datecheck
                break

        for i in range(300):
            datecheck = str(E - datetime.timedelta(i))
            if datecheck in series_contents.keys():
                enddate = datecheck
                break

        for i in series_contents[startdate:enddate].keys():
            yield StockPriceItem(
                                 Symbol='005930', Date=i, Open=series_contents[i][3], Close=series_contents[i][0],
                                 High=series_contents[i][1], Low=series_contents[i][2], Volume=series_contents[i][4],
                                 Cdays=series_contents[i][5]
                                 )

