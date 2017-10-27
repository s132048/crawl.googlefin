from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import stocksymbol.settings

DeclarativeBase =  declarative_base()

def db_connect():

    return create_engine('postgresql://TA:2048@localhost:5432/symboldb')

def create_symbols_table(engine):

    DeclarativeBase.metadata.create_all(engine)



class Symbols(DeclarativeBase):

    __tablename__ = 'symbols'

    company = Column('company', String, primary_key=True)
    exchange = Column('exchange', String)
    symbol = Column('symbol', String)



