구글 파이낸스 데이터 크롤러
==============================================

개요
---------

이 패키지는 `구글 파이낸스 <https://finance.google.com/>`_ 로부터 주식 가격 데이터를 크롤링합니다.

Spider
--------------

SymbolSpder
~~~~~~~~~~~~~~~~~~~

SymbolSpider는 구글 `stock screener <https://finance.google.com/finance?#stockscreener>`_ 에서
주식의 종목명, 종목 코드, 거래소 데이터를 크롤링합니다. 현재 KOSPI, KOSDAQ, NYSE, NASDAQ, TYO, SHE, SHA 를 지원하고 있습니다.
``output=json`` 쿼리를 사용해 json 형태의 파일을 받은 후 모든 텍스트 데이터를 text_contents 리스트에 저장합니다.
먼저 text_contents 로부터 총 종목수를 찾은 후 자료 구조를 파악합니다. 추출된 데이터는 StockSymbolItem 으로 보내집니다.
보내진 데이터는 파이프라인을 통해 PostgreSQL 데이터베이스에 저장됩니다. 테이블을 생성하고 데이터를 삽입하는데 sqlalchemy가 사용 되었습니다.

PriceSpider
~~~~~~~~~~~~~~~~~~~~

PriceSpider는 구글의 get prices 기능을 사용해 주가 데이터를 크롤링합니다.
이 크롤러에서 사용한 get prices 의 쿼리는 아래와 같습니다.

.. line-block::

    https://finance.google.com/finance/getprices?q=005930&x=KRX&p=5Y&f=d,c,v,k,o,h,l
    위 url 은 request 에 사용된 url 예시입니다.
    q 는 종목의 symbol 을 받는 부분으로 예시의 005930은 삼성전자입니다.
    x 는 종목이 속한 거래소를 받는 부분으로 KRX 는 KOSPI 입니다.
    p 는 주가 기록을 받아오는 기간으로 5Y 는 5년을 의미합니다. startdate 로 입력된 인수와 코드를 실행하는 날짜를 계산해 적절한 기간을 쿼리로 입력합니다.
    f 는 원하는 데이터의 형식으로 d (date), c (close), v (volume), k (cdays), o (open), h (high), l (low) 를 의미합니다.


데이터를 얻고자 하는 기간은 scrapy 의 인수로 받습니다. 다음과 같은 커맨드를 사용합니다.

.. code-block::

    scrapy crawl getprices -a startdate='startdate' -a enddate='enddate'

각각의 날짜 인수는 ISO8601 형식만을 지원합니다.




테이블
--------

* stocksymbol

    +----------+------------+
    |  column  |    type    |
    +----------+------------+
    | company  |   varchar  |
    +----------+------------+
    | symbol   |   varchar  |
    +----------+------------+
    | exchange |   varchar  |
    +----------+------------+


* stockprice

    +------------+------------+
    |   column   |   type     |
    +------------+------------+
    |    date    |  varchar   |
    +------------+------------+
    |    open    |   float    |
    +------------+------------+
    |   close    |   float    |
    +------------+------------+
    |    high    |   float    |
    +------------+------------+
    |    low     |   float    |
    +------------+------------+
    |   volume   |    int     |
    +------------+------------+
    |   cdays    |    int     |
    +------------+------------+
