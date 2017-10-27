# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from googlefin.models import Symbols, db_connect, create_symbols_table

class StocksymbolPipeline(object):
    def process_item(self, item, spider):
        return item

class StockScreenerPipeline(object):

    def __init__(self):

        engine = db_connect()
        create_symbols_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        session = self.Session()
        symbol = Symbols(company=item.get('Company'), symbol=item.get('Symbol'), exchange=item.get('Exchange'))

        try:
            session.add(symbol)
            session.commit()

        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item


