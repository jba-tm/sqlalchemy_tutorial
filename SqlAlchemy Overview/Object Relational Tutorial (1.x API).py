# Object Relational Tutorial (1.x API)

# Version Check
# import sqlalchemy
#
# print(sqlalchemy.__version__)
from pprint import pprint

from sqlalchemy import create_engine, Sequence
from sqlalchemy.orm import declarative_base, sessionmaker, aliased, relationship, selectinload, joinedload, \
    contains_eager
from sqlalchemy import Column, Integer, String, text, ForeignKey, Table, Text
from sqlalchemy.sql import func, exists

engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, )
    name = Column(String, )
    fullname = Column(String, )
    nickname = Column(String, )

    addresses = relationship('Address', back_populates='user', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='addresses')

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')

session.add(ed_user)

our_user = session.query(User).filter_by(name='ed').first()

session.add_all([
    User(name='wendy', fullname='Wendy Williams', nickname='windy'),
    User(name='mary', fullname='Mary Contrary', nickname='mary'),
    User(name='fred', fullname='Fred Flintstone', nickname='freddy')])

ed_user.nickname = 'eddie'

session.commit()

ed_user.name = 'Edwardo'
fake_user = User(name='fakeuser', fullname='Invalid', nickname='12345')
session.add(ed_user)

pprint(session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all())

session.rollback()
print(ed_user.name)

print(fake_user in session)

print(session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all())

for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.fullname, instance.nickname)

for name, fullname in session.query(User.name, User.fullname):
    print(name, fullname)

for row in session.query(User, User.name).all():
    print(row.User, row.name)

for row in session.query(User.name.label('name_label')).all():
    print(row.name_label)

user_alias = aliased(User, name='user_alias')

for row in session.query(user_alias, user_alias.name).all():
    print(row.user_alias)

for row in session.query(User).all()[:]:
    print(row)

for name, in session.query(User.name).filter_by(fullname='Ed Jones'):
    print(name)

for name, in session.query(User.name).filter(User.fullname == 'Ed Jones'):
    print(name)

for user in session.query(User).filter(User.fullname == 'Ed Jones').filter(User.name == 'ed'):
    print(user)

print('\nUsing Textual SQL')
for user in session.query(User).filter(text('id<224')).order_by(text('id')).all():
    print(user)

print('\nBind params')
for user in session.query(User).filter(text('id<:value and name=:name')).params(value=224, name='fred').order_by(
        User.id).all():
    print(user)

print('\nWith sql query')
stmt = text("SELECT name, id, fullname, nickname FROM users where name=:name")
stmt = stmt.columns(User.name, User.id, User.fullname, User.nickname)
result = session.query(User).from_statement(stmt).params(name='ed').all()

print('\nCounting')
count = session.query(User).filter(User.name.like('%ed')).count()
print(count)

print('\nBuilding a Relationship')

jack = User(name='jack', fullname='Jack Bean', nickname='gjffdd')

print('\nWorking with Related Objects')
print(jack.addresses)

jack.addresses = [
    Address(email_address='jack@google.com'),
    Address(email_address='j25@yahoo.com')]

print(jack.addresses)

session.add(jack)
session.commit()

jack = session.query(User).filter_by(name='jack').one()
print(jack)

print(jack.addresses)

print('\nQuerying with Joins')
for u, a in session.query(User, Address).filter(User.id == Address.user_id).filter(
        Address.email_address == 'jack@google.com').all():
    print(u)
    print(a)

result = session.query(User).join(Address).filter(Address.email_address == 'jack@google.com').all()
print(result)

print('\nUsing Aliases')
adalias1 = aliased(Address)
adalias2 = aliased(Address)
for username, email1, email2 in session.query(User.name, adalias1.email_address, adalias2.email_address).join(
        User.addresses.of_type(adalias1)).join(User.addresses.of_type(adalias2)).filter(
    adalias1.email_address == 'jack@google.com').filter(adalias2.email_address == 'j25@yahoo.com'):
    print(username, email1, email2)

print('\nUsing Subqueries')
stmt = session.query(Address.user_id, func.count('*').label('address_count')).group_by(Address.user_id).subquery()

for u, count in session.query(User, stmt.c.address_count).outerjoin(stmt, User.id == stmt.c.user_id).order_by(User.id):
    print(u, count)

print('\nSelecting Entities from Subqueries')
stmt = session.query(Address).filter(Address.email_address != 'j25@yahoo.com').subquery()

adalias = aliased(Address, stmt)

for user, address in session.query(User, adalias).join(adalias, User.addresses):
    print(user)
    print(address)

print('\nUsing EXISTS')
stmt = exists().where(Address.user_id == User.id)
for name, in session.query(User.name).filter(stmt):
    print(name)

for name, in session.query(User.name).filter(User.addresses.any()):
    print(name)

print('\nEager Loading')
print('Selectin Load')
jack = session.query(User).options(selectinload(User.addresses)).filter_by(name='jack').one()
print(jack)
print(jack.addresses)

print('\nJoined Load')
jack = session.query(User).options(joinedload(User.addresses)).filter_by(name='jack').one()
print(jack)

print('\nExplicit Join + Eagerload')
jacks_addresses = session.query(Address).join(Address.user).filter(User.name == 'jack').options(
    contains_eager(Address.user)).all()
print(jacks_addresses)

print(jacks_addresses[0].user)

print('\Deleting')
session.delete(jack)
result = session.query(User).filter_by(name='jack').count()
print(result)

result = session.query(Address).filter(Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])).count()
print(result)

print('\nBuilding a Many To Many Relationship')

# post_keywords = Table(
#     'post_keywords', Base.meetadata,
#     Column('post_id', ForeignKey('posts.id'), primary_key=True),
#     Column('keyword_id', ForeignKey('keywords.id'), primary_key=True),
# )
#
# class BlogPost(Base):
#     __tablename__ = 'posts'
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     headline = Column(String(255), nullable=False)
#     body = Column(Text)
#     keywords = relationship('Keyword', secondary=post_keywords, back_populates='posts')
#
#     def __init__(self, headline, body, author):
#         self.author = author
#         self.headline = headline
#         self.body = body
#
#     def __repr__(self):
#         return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)
#
# class Keyboard(Base):
#     __tablename = 'keywords'
#
#     id = Column(Integer, primary_key=True)
#     keyword = Column(String(50), nullable=False, unique=True)
#     posts = relationship('BlogPost', secondary=post_keywords, back_populates='keywords')
#
#     def __init__(self, keyword):
#         self.keyword = keyword
#
#
# BlogPost.author = relationship(User, back_populates="posts")
# User.posts = relationship(BlogPost, back_populates="author", lazy="dynamic")
#
#
# Base.metadata.create_all(engine)

