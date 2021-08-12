from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from .database import Base

association_table = Table(
    'association',
    Base.metadata,
    Column('lesson_id', Integer, ForeignKey('lessons.id')),
    Column('group_id', Integer, ForeignKey('groups.id')),
)


class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    lesson_title = Column(String)
    groups = relationship('Group', secondary=association_table, backref='group_lesson')

    def __repr__(self):
        return f'Lesson [Id: {self.id}, Name: {self.lesson_title}]'
