from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Publications(Base):
    __tablename__ = "annual_reports_publications"

    id = Column(Integer, primary_key=True)
    publications = Column(Integer, nullable=False)
    journals = Column(Integer, nullable=False)
    contributions = Column(Integer, nullable=False)
    theses = Column(Integer, nullable=False)
    rest = Column(Integer, nullable=False)
    year = Column(Date, nullable=False)


class Categories(Base):
    __tablename__ = "annual_reports_categories"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    count = Column(Integer, nullable=False)
    year = Column(Date, nullable=False)


class Journals(Base):
    __tablename__ = "annual_reports_journals"

    id = Column(Integer, primary_key=True)
    journal = Column(String, nullable=False)
    count = Column(Integer, nullable=False)
    year = Column(Date, nullable=False)
