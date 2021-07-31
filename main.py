# Object Relational Tutorial (1.x API)

# Version Check
# import sqlalchemy
#
# print(sqlalchemy.__version__)


from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, )
    name = Column(String, )
    fullname = Column(String, )
    nickname = Column(String, )

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)
