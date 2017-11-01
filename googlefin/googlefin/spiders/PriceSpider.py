import scrapy
import csv
import datetime
import pandas as pd
from ..items import StockPriceItem
from dateutil.parser import parse

class PriceSpider(scrapy.Spider):
    name = 'getprices'

    def start_requests(self):

        symbols = pd.read_csv('/Users/TA/Veranos/crawl.googlefin/googlefin/googlefin/symbols/symbols.csv')
        symbols.index = symbols['Company']
        del symbols['Company']

        urls = {}
        url = 'https://finance.google.com/finance/getprices?q=%s&x=%s&p=%sY&f=d,c,v,k,o,h,l'

        S = parse(self.startdate).date()
        duration = datetime.datetime.now().date() - S
        D = duration.days//365 + 1

        if (self.code == 'all') & (self.ex == 'all'):
            for company, symbol in symbols.iterrows():
                urls[company] = url %(symbol['Symbol'], symbol['Exchange'], D)

        if (self.code == 'all') & (self.ex != 'all'):
            symbols = symbols[symbols['Exchange'] == self.ex]
            for company, symbol in symbols.iterrows():
                urls[company] = url %(symbol['Symbol'], symbol['Exchange'], D)

        if (self.code != 'all') & (self.ex != 'all'):
            company = symbols[(symbols['Exchange']==self.ex)&(symbols['Symbol']==self.code)].index[0]
            urls[company] = url %(self.code, self.ex, D)

        for i in urls:
            yield scrapy.Request(url=urls[i], callback=self.parse, meta={'company': i})




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
                                 Symbol=response.meta['company'],
                                 Date=i, Open=series_contents[i][3], Close=series_contents[i][0],
                                 High=series_contents[i][1], Low=series_contents[i][2],
                                 Volume=series_contents[i][4], Cdays=series_contents[i][5]
                                 )

