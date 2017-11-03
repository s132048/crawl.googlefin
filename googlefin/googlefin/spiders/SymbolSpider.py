import scrapy
import csv
from ..items import StockSymbolItem

class SymbolSpider(scrapy.Spider):

    name = 'stock_symbol'

    def start_requests(self):
        urls = {
                "KR": {
                    "KOSPI" : "https://finance.google.com/finance?" +
                              "output=json&start=0&num=5000&" +
                              "q=[currency%20%3D%3D%20%22KRW%22%20%26%20%28exchange%20%3D%3D%20%22" +
                              "KRX%22%29%20%26%20%28" +
                              "dividend_yield%20%3E%3D%200%29%20%26%20%28" +
                              "dividend_yield%20%3C%3D%201000%29]&restype=company",
                    "KOSDAQ" : "https://finance.google.com/finance?" +
                               "output=json&start=0&num=5000&" +
                               "q=[currency%20%3D%3D%20%22KRW%22%20%26%20%28exchange%20%3D%3D%20%22" +
                               "KOSDAQ%22%29%20%26%20%28" +
                               "dividend_yield%20%3E%3D%200%29%20%26%20%28" +
                               "dividend_yield%20%3C%3D%201000%29]&restype=company",
                },
                "US": {
                    "NYSE": "https://finance.google.com/finance?" +
                            "output=json&start=0&num=5000&" +
                            "q=[currency%20%3D%3D%20%22USD%22%20%26%20%28exchange%20%3D%3D%20%22" +
                            "NYSE%22%29%20%26%20%28" +
                            "dividend_yield%20%3E%3D%200%29%20%26%20%28" +
                            "dividend_yield%20%3C%3D%201000%29]&restype=company",
                    "NASDAQ": "https://finance.google.com/finance?" +
                              "output=json&start=0&num=5000&" +
                              "q=[currency%20%3D%3D%20%22USD%22%20%26%20%28exchange%20%3D%3D%20%22" +
                              "NASDAQ%22%29%20%26%20%28" +
                              "dividend_yield%20%3E%3D%200%29%20%26%20%28" +
                              "dividend_yield%20%3C%3D%201000%29]&restype=company",
                },
                "JP": {
                    "TYO": "https://finance.google.com/finance?" +
                           "output=json&start=0&num=5000&" +
                           "q=[currency%20%3D%3D%20%22JPY%22%20%26%20%28" +
                           "exchange%20%3D%3D%20%22TYO%22%29%20%26%20%28" +
                           "dividend_yield%20%3E%3D%200%29%20%26%20%28" +
                           "dividend_yield%20%3C%3D%201000%29]&restype=company",
                },
                "CN": {
                    "SHA": "https://finance.google.com/finance?" +
                           "output=json&start=0&num=5000&" +
                           "q=[%28exchange%20%3D%3D%20%22SHA%22%29%20%26%20%28" +
                           "dividend_yield%20%3E%3D%200%29%20%26%20%28" +
                           "dividend_yield%20%3C%3D%208.62%29]&restype=company",
                    "SHE": "https://finance.google.com/finance?" +
                           "output=json&start=0&num=5000&" +
                           "q=[%28exchange%20%3D%3D%20%22SHE%22%29%20%26%20%28" +
                           "dividend_yield%20%3E%3D%200%29%20%26%20%28" +
                           "dividend_yield%20%3C%3D%208.56%29]&restype=company",
                },
        }
        for country in urls:
            for url in urls[country].values():
                yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.text
        read = csv.reader(page)
        text_contents = []

        for i in read:
            text_contents.append(i)

        company_count = 0
        startpoint = 0
        exchange_symbol = 'exchange_id'

        for i in range(len(text_contents)):
            if text_contents[i] == ['num_company_results']:
                company_count = int(text_contents[i + 4][0])
            elif text_contents[i] == ['title']:
                startpoint = i
            elif text_contents[i] == ['exchange']:
                exchange_symbol = text_contents[i + 4][0]
                break

        text_contents = text_contents[startpoint:]
        gap = int(len(text_contents)/company_count)

        def escape_html(text):
            return text \
                    .replace('\\u0026', '&') \
                    .replace('\\u0027', "'") \
                    .replace('\\u002F', '/') \
                    .replace('\\u003B', ',') \
                    .replace('\\u0022', '"')

        for i in range(company_count):
            name = text_contents[i * gap+4][0]
            name = escape_html(name)
            symbol = text_contents[i * gap + 25][0]
            yield StockSymbolItem(symbol=symbol, name=name, exchange_symbol=exchange_symbol)





