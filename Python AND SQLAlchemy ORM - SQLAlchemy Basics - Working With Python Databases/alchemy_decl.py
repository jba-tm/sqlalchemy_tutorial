from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

engine = create_engine('sqlite:///sqlite2.db', echo=True)
# engine = create_engine('sqlite:///sqlite.db', echo=True)
Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    genre = Column(String(255, ), default='')
    price = Column(Integer, nullable=False)
    author = relationship('Author')


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, ), nullable=False)
    books = relationship('Book')


Base.metadata.create_all(engine)
