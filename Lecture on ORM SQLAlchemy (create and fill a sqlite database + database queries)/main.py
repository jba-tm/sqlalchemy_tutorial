import os

from sqlalchemy import and_

from models.database import DATABASE_NAME, Session
from create_database import create_database
from models.lesson import Lesson, association_table
from models.group import Group
from models.student import Student

if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        create_database()

    session = Session()

    for it in session.query(Lesson):
        print(it)

    print('*' * 30)

    for it in session.query(Lesson).filter(Lesson.id > 1):
        print(it)

    print('*' * 30)
    for it in session.query(Lesson).filter(and_(Lesson.id >= 1, Lesson.lesson_title.like('P%'))):
        print(it)
    print('*' * 30)
    for student in session.query(Student).join(Group).filter(Group.group_name == '1-MDA-9'):
        print(student)
    print('*' * 30)

    for student, group in session.query(Student, Group):
        print(student, group)
    print('*' * 30)

    for it, group in session.query(Lesson.lesson_title, Group.group_name).filter(and_(
        association_table.c.lesson_id == Lesson.id,
        association_table.c.group_id == Group.id,
        Group.group_name == '1-MDA-9'
    )):
        print(it, group)
    print('*' * 30)
