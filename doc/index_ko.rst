구글 파이낸스 데이터 크롤러
==============================================

개요
---------

이 패키지는 `구글 파이낸스 <https://finance.google.com/>`_ 로부터 주식 가격 데이터를 크롤링합니다.

stocksymbol
-------------

stocksymbol 스파이더는 구글 `stock screnner <https://finance.google.com/finance?#stockscreener>`_ 에서
주식의 종목명, 종목 코드, 거래소 데이터를 크롤링합니다. 현재 KOSPI, KOSDAQ, NYSE, NASDAQ, TYO, SHE, SHA 를 지원하고 있습니다.
``output=json`` 쿼리를 사용해 json 형태의 파일을 받은 후 모든 텍스트 데이터를 text_contents 리스트에 저장합니다.
먼저 text_contents 로부터 총 종목수를 찾은 후 자료 구조를 파악합니다. 추출된 데이터는 StockSymbolItem 에 저장됩니다.


테이블
--------

* stodksymbol

    +----------+------------+
    |  column  |    type    |
    +----------+------------+
    | company  |   varchar  |
    +----------+------------+
    | symbo l  |   varchar  |
    +----------+------------+
    | exchange |   varchar  |
    +----------+------------+