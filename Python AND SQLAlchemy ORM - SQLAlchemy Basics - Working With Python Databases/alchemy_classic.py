from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey

meta = MetaData()

authors = Table(
    'authors', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=True, default='', )
)

books = Table('books', meta,
              Column('id', Integer, primary_key=True),
              Column('name', String(255), ),
              Column('genre', String(255), ),
              Column('author_id', Integer, ForeignKey('authors.id')),
              Column('price', Integer),
              )

print(books.c.author_id)
print(books.primary_key)

print(authors.c.name)
print(authors.primary_key)
print(authors.c)

engine = create_engine('sqlite:///sqlite.db', echo=True)
meta.create_all(engine)

conn = engine.connect()

ins_author_query = authors.insert().values(name='Lutz')
conn.execute(ins_author_query)

ins_book_query = books.insert().values(name='Learn Python', author_id=1, genre='Education', price=1299)
conn.execute(ins_book_query)
ins_book_query2 = books.insert().values(name='Clear Python', author_id=1, genre='Education', price=956)
conn.execute(ins_book_query2)

books_gr_1000_query = books.select().where(books.c.price > 1000)
result = conn.execute(books_gr_1000_query)

for row in result:
    print(row)

s = select([books, authors]).where(books.c.author_id == authors.c.id)

result = conn.execute(s)

print()

for row in result:
    print(row)
