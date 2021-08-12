from sqlalchemy import Column, Integer, String, ForeignKey

from .database import Base


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, default='', )
    surname = Column(String, default='')
    patronymic = Column(String, default='')
    age = Column(Integer, nullable=True)
    address = Column(String, default='', )
    group = Column(Integer, ForeignKey('groups.id'))

    def __init__(self, full_name: str, age: int, address: str, id_group: int):
        self.surname = full_name[0]
        self.name = full_name[1]
        self.patronymic = full_name[2]
        self.age = age
        self.address = address
        self.group = id_group

    def __repr__(self):
        info: str = f'Student [Fullname: {self.surname} {self.name} {self.patronymic}, ' \
                    f'Age: {self.age}, Address: {self.address}, Id group: {self.group}]'
        return info
