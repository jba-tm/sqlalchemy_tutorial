from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alchemy_decl import Base, Book, Author

engine = create_engine('sqlite:///sqlite2.db')

Session = sessionmaker(engine)

session = Session()

author_one = Author(name='Lutz')

session.add(author_one)
session.commit()

book_one = Book(title='Clear Python', author_id=1, genre='Computer technique', price=2500)

