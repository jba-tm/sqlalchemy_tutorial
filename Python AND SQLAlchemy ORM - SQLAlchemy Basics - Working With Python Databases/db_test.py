from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, and_

engine = create_engine('sqlite:///sqlite.db')
meta = MetaData(engine)

authors = Table('authors', meta, autoload=True)
books = Table('books', meta, autoload=True)

conn = engine.connect()
s = select((books, authors)).where(and_(books.c.author_id == authors.c.id, books.c.price > 1200))
result = conn.execute(s)

for row in result.fetchall():
    print(row)

delete_query = books.delete().where(books.c.id == 1)
conn.execute(delete_query)

update_query = books.update().where(books.c.id == 2, ).values(name='AnotherTitle')
conn.execute(update_query)

##################################################################################
from sqlalchemy.orm import mapper, relationship, sessionmaker

engine = create_engine('sqlite:///sqlite.db', echo=True)
meta = MetaData(engine)

authors = Table('authors', meta, autoload=True)
books = Table('books', meta, autoload=True)


class Book(object):
    def __init__(self, title, author_id, genre, price):
        self.title = title
        self.author_id = author_id
        self.genre = genre
        self.price = price


class Author(object):
    def __init__(self, name):
        self.name = name


mapper(Book, books)
mapper(Author, authors)

new_book = Book('NewBook', 1, 'NewG', 2500)

DBSession = sessionmaker(bind=engine)
session = DBSession()
session.add(new_book)
session.commit()

for row in session.query(Book).filter(Book.price > 1000):
    print(row.name)

for row in session.query(Book, Author).filter(Book.author_id == Author.id).filter(Book.price > 1000):
    print(row.Book.name, ' ', row.Author.name)

print()

second_book = session.query(Book).filter_by(id=3).one()

if second_book != []:
    second_book.price = 3000
    session.add(second_book)
    session.commit()

second_book = session.query(Book).filter_by(id=2).one()
if second_book:
    print(second_book)
    session.delete(second_book)
    session.commit()

try:
    query_res = session.query(Book).filter_by(id=2).one()
except Exception as e:
    print(e)
else:
    print(query_res.price)


