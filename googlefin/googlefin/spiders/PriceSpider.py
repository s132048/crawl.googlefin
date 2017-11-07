import scrapy
import csv
import datetime
import pandas as pd
from ..items import StockPriceItem
from dateutil.parser import parse

class PriceSpider(scrapy.Spider):
    name = 'stock_daily_price'
    custom_settings = {
        'DOWNLOAD_DELAY':1.00
    }

    def start_requests(self):

        symbols = pd.read_csv('/Users/TA/Veranos/crawl.googlefin/googlefin/googlefin/symbols/symbols.csv')
        symbols.index = symbols['name']
        del symbols['name']

        urls = {}
        url = 'https://finance.google.com/finance/getprices?q=%s&x=%s&p=%sY&f=d,c,v,k,o,h,l'

        startdate = parse(self.startdate).date()
        duration = datetime.datetime.now().date() - startdate
        year = duration.days//365 + 1

        if (self.symbol == 'all') & (self.exchange == 'all'):
            for name, symbol in symbols.iterrows():
                urls[name] = [url %(symbol['symbol'], symbol['exchange_symbol'], year), symbol['exchange_symbol']]

        if (self.symbol == 'all') & (self.exchange != 'all'):
            symbols = symbols[symbols['exchange_symbol'] == self.exchange]
            for name, symbol in symbols.iterrows():
                urls[name] = [url %(symbol['symbol'], symbol['exchange_symbol'], year), symbol['exchange_symbol']]

        if (self.symbol != 'all') & (self.exchange != 'all'):
            symbol_input = self.symbol.split(sep=',')
            for symbol in symbol_input:
                name = symbols[(symbols['exchange_symbol']==self.exchange)&(symbols['symbol']==symbol)].index[0]
                urls[name] = [url %(symbol, self.exchange, year), self.exchange]

        for name in urls:
            yield scrapy.Request(url=urls[name][0], callback=self.parse, meta={'name': name, 'exchange_symbol': urls[name][1]})




    def parse(self, response):
        page = response.text
        startdate = parse(self.startdate).date()
        enddate = parse(self.enddate).date()


        list_contents = []
        series_contents = pd.Series()
        page = csv.StringIO(page)
        page = csv.reader(page)

        for line in page:

            if len(line) == 7:
                list_contents.append(line)

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
            datecheck = str(startdate + datetime.timedelta(i))
            if datecheck in series_contents.keys():
                startdate = datecheck
                break

        for i in range(300):
            datecheck = str(enddate - datetime.timedelta(i))
            if datecheck in series_contents.keys():
                enddate = datecheck
                break

        for i in series_contents[startdate:enddate].keys():
            yield StockPriceItem(
                                 name=response.meta['name'], exchange_symbol=response.meta['exchange_symbol'],
                                 date=i, open=series_contents[i][3], close=series_contents[i][0],
                                 high=series_contents[i][1], low=series_contents[i][2],
                                 volume=series_contents[i][4], cdays=series_contents[i][5]
                                 )

