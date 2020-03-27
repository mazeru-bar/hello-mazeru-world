from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.database import Base
from datetime import datetime


class DBContent(Base):
    __tablename__ = 'DBcontents'
    id = Column(Integer, primary_key=True)
    title = Column(String(128), unique=True)
    body = Column(Text)
    date = Column(DateTime, default=datetime.now())


    def __init__(self, title=None, body=None, date=None):
        self.title = title
        self.body = body
        self.date = date

    def __repr__(self):
        #return '<Title %r>' % (self.title)
        return "{} {} {}".format(slf.body, self.title, self.date)
