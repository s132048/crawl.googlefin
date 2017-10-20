google finance crawler
==============================================

overview
---------
This package crawl financial data from google finance.

stocksymbol
-------------
Stocksymbol's spider crawls each stock's company name, stock symbol and exchange id.
To get data, it uses `google stock screnner <https://finance.google.com/finance?#stockscreener>`_ feature.
Now it supports KOSPI, KOSDAQ, NYSE, NASDAQ, TYO, SHE and SHA.
After getting data in JSON format, it parses


테이블
--------
* symbol_exchange

+----------+------------+
|  column  |    type    |
+----------+------------+
|  company |   varchar  |
+----------+------------+
|  symbol  |   varchar  |
+----------+------------+
| exchange |   varchar  |
+----------+------------+