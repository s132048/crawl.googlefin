import scrapy
import csv
from ..items import StockSymbolItem

class SymbolSpider(scrapy.Spider):
    name = 'getsymbols'
    def start_requests(self):
        urls = {
                "KR": {
                    "KOSPI" : 'https://finance.google.com/finance?output=json&start=0&num=5000&q=[currency%20%3D%3D%20%22KRW%22%20%26%20%28exchange%20%3D%3D%20%22KRX%22%29%20%26%20%28dividend_yield%20%3E%3D%200%29%20%26%20%28dividend_yield%20%3C%3D%201000%29]&restype=company',
                    "KOSDAQ" : 'https://finance.google.com/finance?output=json&start=0&num=5000&q=[currency%20%3D%3D%20%22KRW%22%20%26%20%28exchange%20%3D%3D%20%22KOSDAQ%22%29%20%26%20%28dividend_yield%20%3E%3D%200%29%20%26%20%28dividend_yield%20%3C%3D%201000%29]&restype=company',
                    },
                "US": {
                    "NYSE": 'https://finance.google.com/finance?output=json&start=0&num=5000&q=[currency%20%3D%3D%20%22USD%22%20%26%20%28exchange%20%3D%3D%20%22NYSE%22%29%20%26%20%28dividend_yield%20%3E%3D%200%29%20%26%20%28dividend_yield%20%3C%3D%201000%29]&restype=company',
                    "NASDAQ": 'https://finance.google.com/finance?output=json&start=0&num=5000&q=[currency%20%3D%3D%20%22USD%22%20%26%20%28exchange%20%3D%3D%20%22NASDAQ%22%29%20%26%20%28dividend_yield%20%3E%3D%200%29%20%26%20%28dividend_yield%20%3C%3D%201000%29]&restype=company',
                    },
                "JP": {
                    "TYO": 'https://finance.google.com/finance?output=json&start=0&num=5000&q=[currency%20%3D%3D%20%22JPY%22%20%26%20%28exchange%20%3D%3D%20%22TYO%22%29%20%26%20%28dividend_yield%20%3E%3D%200%29%20%26%20%28dividend_yield%20%3C%3D%201000%29]&restype=company',
                    },
                "CN": {
                    "SHA": 'https://finance.google.com/finance?output=json&start=0&num=5000&q=[%28exchange%20%3D%3D%20%22SHA%22%29%20%26%20%28dividend_yield%20%3E%3D%200%29%20%26%20%28dividend_yield%20%3C%3D%208.62%29]&restype=company',
                    "SHE": 'https://finance.google.com/finance?output=json&start=0&num=5000&q=[%28exchange%20%3D%3D%20%22SHE%22%29%20%26%20%28dividend_yield%20%3E%3D%200%29%20%26%20%28dividend_yield%20%3C%3D%208.56%29]&restype=company'
                }
        }
        for country in urls:
            for url in urls[country].values():
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.text
        read = csv.reader(page)
        text_contents = []
        SSI = StockSymbolItem

        for i in read:
            text_contents.append(i)

        company_count = 0
        startpoint = 0
        exchange = 'exchange_id'

        for i in range(len(text_contents)):
            if text_contents[i] == ['num_company_results']:
                company_count = int(text_contents[i+4][0])
            elif text_contents[i] == ['title']:
                startpoint = i
            elif text_contents[i] == ['exchange']:
                exchange = text_contents[i+4][0]
                break

        text_contents = text_contents[startpoint:]
        gap = int(len(text_contents)/company_count)

        for i in range(company_count):
            company = text_contents[i*gap+4][0].replace('\\u0026', '&').replace('\\u0027', "'").replace('\\u002F', '/').replace('\\u003B', ',').replace('\\u0022', '"')
            symbol = text_contents[i*gap+25][0]
            yield SSI(Company = company, Symbol = symbol, Exchange = exchange )





