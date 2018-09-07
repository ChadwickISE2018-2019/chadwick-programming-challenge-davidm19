from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql import func

Base = declarative_base()

class Customer (Base) :
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, autoincrement=True )
    first_name = Column(String(32))
    last_name = Column(String(32))
    email = Column(String(100))

engine = create_engine('sqlite:///data.db')
Base.metadata.create_all(engine)
