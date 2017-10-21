google finance crawler
==============================================

overview
---------

This package crawl financial data from google finance.

stocksymbol
-------------

Stocksymbol's spider crawls each stock's company name, stock symbol and exchange id.
To get data, it uses `google stock screnner <https://finance.google.com/finance?#stockscreener>`_.
Now it supports KOSPI, KOSDAQ, NYSE, NASDAQ, TYO, SHE and SHA.
After getting data in JSON format, it parses to a list named test_contents.
The list contains all the text data from the JSON format.
Spider finds numbers of companies in each exchange.
Then it interprets a construct of the list.
It yields data to StockSymbolItem object.



Table
--------

* symbols

+----------+------------+
|  column  |    type    |
+----------+------------+
|  company |   varchar  |
+----------+------------+
|  symbol  |   varchar  |
+----------+------------+
| exchange |   varchar  |
+----------+------------+