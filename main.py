# Inserting Rows with Core

from sqlalchemy import insert
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import create_engine

metadata = MetaData()
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)


user_table = Table(
    "user_account",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('fullname', String)
)

stmt = insert(user_table).values(name='spongebob', fullname="Spongebob Squarepants")

with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()
