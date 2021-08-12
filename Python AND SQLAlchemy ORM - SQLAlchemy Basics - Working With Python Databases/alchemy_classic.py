from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey

meta = MetaData()

authors = Table(
    'Authors', meta,
    Column('id_author', Integer, primary_key=True),
    Column('name', String, nullable=True, default='', )
)

books = Table('Books', meta,
              Column(),
              )