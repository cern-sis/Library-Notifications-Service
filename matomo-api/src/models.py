from sqlalchemy import Column, Date, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MatomoData(Base):
    __tablename__ = "inspire_matomo_data"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    visits = Column(Integer)
    unique_visitors = Column(Integer)
