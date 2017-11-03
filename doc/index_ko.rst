구글 파이낸스 데이터 크롤러
==============================================

개요
---------

이 패키지는 `구글 파이낸스 <https://finance.google.com/>`_ 로부터 주식 가격 데이터를 크롤링합니다.

Spider
--------------

SymbolSpder
~~~~~~~~~~~~~~~~~~~

SymbolSpider는 구글 `stock screener <https://finance.google.com/finance?#stockscreener>`_ 에서 주식의 종목명, 종목 코드, 거래소 데이터를 크롤링합니다.
현재 KOSPI(KRX), KOSDAQ, NYSE, NASDAQ, TYO, SHE, SHA 를 지원하고 있습니다.

``output=json`` 쿼리를 사용해 json 형태의 파일을 받은 후 모든 텍스트 데이터를 text_contents 리스트에 저장합니다.
먼저 text_contents 로부터 총 종목수를 찾은 후 자료 구조를 파악합니다. 추출된 데이터는 StockSymbolItem 으로 보내집니다.
보내진 데이터는 파이프라인을 통해 PostgreSQL 데이터베이스에 저장됩니다. 테이블을 생성하고 데이터를 삽입하는데 sqlalchemy가 사용 되었습니다.

다음 코드는 크롤링에 사용된 예시입니다.

.. code-block::

    scrapy crawl stock_symbol -a exchange='SHA,SHE'

exchange 인수로 크롤링하고자 하는 거래소를 지정합니다. 사용 가능한 인수는 KRX, KOSDAQ, NYSE, NASDAQ, SHA, SHE, TYO 입니다.
거래소명은 공백 없이 ``,`` 로 나누어 입력합니다. 'all' 을 입력하면 지원하는 모든 거래소로부터 크롤링합니다.



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


PriceSpider 는 총 세가지 모드를 지원합니다.

특정 종목 크롤링
^^^^^^^^^^^^^^^^^^^^^^

크롤링 하고자 하는 종목이 하나일 경우 다음 커맨드를 사용합니다.

.. code-block::

    scrapy crawl stock_price -a symbol='005930,035720' -a exchange='KRX' -a startdate='2016-11-01' -a enddate='2017-11-01'

symbol 인수는 종목 코드를 받습니다. 종목이 속한 거래소는 exchange 인수를 통해 받습니다.
예시로 사용된 커맨드는 KRX 거래소의 005930 종목과 035720 종목을 크롤링합니다.
여러 종목의 크롤링을 원한다면 symbol 인수에 ``,`` 로 구분하여 공백없이 입력합니다.
symbol 테이블에 거래소와 종목 코드가 모두 일치하는 종목이 없다면 크롤링 되지 않습니다.
startdate 와 enddate 인수는 크롤링하고자 하는 기간을 지정합니다.
위 예시는 2016년 11월 1일부터 2017년 11월 1일까지의 기록을 크롤링 합니다.
날짜는 반드시 ISO 8601 형식으로 입력 되어야 합니다. 기간을 지정하는 인수는 모든 모드에서 동일하게 사용됩니다.

특정 거래소 크롤링
^^^^^^^^^^^^^^^^^^^^^^^^^

특정 거래소의 모든 종목을 크롤링 하고자 한다면 다음 커맨드를 사용합니다.

.. code-block::

    scrapy crawl getprices -a symbol='all' -a exchange='KRX' -a startdate='2016-11-01' -a enddate='2017-11-01'

exchange 인수에 원하는 거래소를 입력하고 symbol 인수에 'all' 을 입력하면 입력된 거래소에 속한 모든 종목의 가격 정보를 크롤링합니다.
예시로 사용된 커맨드는 KRX 거래소의 모든 종목을 크롤링합니다.
exchange 인수로 사용가능한 거래소는 KRX, KOSDAQ, TYO, SHE, SHA, NYSE, NASDAQ 이 있습니다.

모든 종목 크롤링
^^^^^^^^^^^^^^^^^^^^^

symbols 테이블에 있는 모든 종목을 크롤링 하고자 한다면 다음 커맨드를 사용합니다.

.. code-block::

    scrapy crawl getprices -a symbol='all' -a exchange='all' -a startdate='2016-11-01' -a enddate='2017-11-01'

위 커맨드를 사용하면 KRX, KOSDAQ, TYO, SHA, SHE, NASDAQ, NYSE 거래소에 속한 모든 종목의 가격 기록을 크롤링합니다.




테이블
--------

* stocksymbol

    +-----------------+------------+
    |     column      |    type    |
    +-----------------+------------+
    |      name       |   varchar  |
    +-----------------+------------+
    |     symbol      |   varchar  |
    +-----------------+------------+
    | exchange_symbol |   varchar  |
    +-----------------+------------+


* stockprice

    +-----------------+------------+
    |      column     |   type     |
    +-----------------+------------+
    |      symbol     |  varchar   |
    +-----------------+------------+
    | exchange_symbol |  varchar   |
    +-----------------+------------+
    |       date      |  varchar   |
    +-----------------+------------+
    |       open      |   float    |
    +-----------------+------------+
    |       close     |   float    |
    +-----------------+------------+
    |       high      |   float    |
    +-----------------+------------+
    |       low       |   float    |
    +-----------------+------------+
    |      volume     |    int     |
    +-----------------+------------+
    |      cdays      |    int     |
    +-----------------+------------+
