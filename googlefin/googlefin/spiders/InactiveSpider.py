import scrapy
from ..items import InactiveSymbolItem

class InactiveSpider(scrapy.Spider):

    name = 'inactive_symbol'

    def start_requests(self):
        urls = {
                "KOSPI" : "https://finance.google.com/finance?" +
                          "start=0&num=5000&" +
                          "q=[currency%20%3D%3D%20%22KRW%22%20%26%20%28exchange%20%3D%3D%20%22" +
                          "KRX%22%29%20%26%20%28" +
                          "dividend_yield%20%3E%3D%200%29%20%26%20%28" +
                          "dividend_yield%20%3C%3D%201000%29]&restype=company",
                "KOSDAQ" : "https://finance.google.com/finance?" +
                          "start=0&num=5000&" +
                          "q=[currency%20%3D%3D%20%22KRW%22%20%26%20%28exchange%20%3D%3D%20%22" +
                          "KOSDAQ%22%29%20%26%20%28" +
                          "dividend_yield%20%3E%3D%200%29%20%26%20%28" +
                          "dividend_yield%20%3C%3D%201000%29]&restype=company",
                "NYSE": "https://finance.google.com/finance?" +
                          "start=0&num=5000&" +
                          "q=[currency%20%3D%3D%20%22USD%22%20%26%20%28exchange%20%3D%3D%20%22" +
                          "NYSE%22%29%20%26%20%28" +
                          "dividend_yield%20%3E%3D%200%29%20%26%20%28" +
                          "dividend_yield%20%3C%3D%201000%29]&restype=company",
                "NASDAQ": "https://finance.google.com/finance?" +
                          "start=0&num=5000&" +
                          "q=[currency%20%3D%3D%20%22USD%22%20%26%20%28exchange%20%3D%3D%20%22" +
                          "NASDAQ%22%29%20%26%20%28" +
                          "dividend_yield%20%3E%3D%200%29%20%26%20%28" +
                          "dividend_yield%20%3C%3D%201000%29]&restype=company",
                "TYO": "https://finance.google.com/finance?" +
                          "start=0&num=5000&" +
                          "q=[currency%20%3D%3D%20%22JPY%22%20%26%20%28" +
                          "exchange%20%3D%3D%20%22TYO%22%29%20%26%20%28" +
                          "dividend_yield%20%3E%3D%200%29%20%26%20%28" +
                          "dividend_yield%20%3C%3D%201000%29]&restype=company",
                "SHA": "https://finance.google.com/finance?" +
                          "start=0&num=5000&" +
                          "q=[%28exchange%20%3D%3D%20%22SHA%22%29%20%26%20%28" +
                          "dividend_yield%20%3E%3D%200%29%20%26%20%28" +
                          "dividend_yield%20%3C%3D%208.62%29]&restype=company",
                "SHE": "https://finance.google.com/finance?" +
                          "start=0&num=5000&" +
                          "q=[%28exchange%20%3D%3D%20%22SHE%22%29%20%26%20%28" +
                          "dividend_yield%20%3E%3D%200%29%20%26%20%28" +
                          "dividend_yield%20%3C%3D%208.56%29]&restype=company",
                }
        if self.exchange == 'all':
            for url in urls.values():
                yield scrapy.Request(url=url, callback=self.parse)
        else:
            for exchange_symbol in self.exchange.split(sep=','):
                if exchange_symbol in urls.keys():
                    yield scrapy.Request(url=urls[exchange_symbol], callback=self.parse)


    def parse(self, response):
        exchange_symbol = response.xpath('//*[@id="gf-viewc"]/div/div[3]/form/table/tr[1]/td[2]/text()').extract()[0][:-1]
        page = response.text

        list_contents = page.split(sep="Inactive")[1:]
        for i in list_contents:
            inactive_symbols = i.split(sep='<nobr>\n')[1]
            symbol = inactive_symbols.split(sep='</n')[0]
            yield InactiveSymbolItem(symbol=symbol, exchange_symbol=exchange_symbol)





