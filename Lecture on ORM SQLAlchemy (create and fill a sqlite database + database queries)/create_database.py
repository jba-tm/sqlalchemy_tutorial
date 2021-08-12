from faker import Faker

from models.database import create_db, Session
from models.lesson import Lesson
from models.group import Group
from models.student import Student

__all__ = ('create_database',)


def create_database(load_fake_data: bool = True):
    create_db()
    if load_fake_data:
        _load_fake_data(Session())


def _load_fake_data(session: Session):
    lessons_names = ('Math', 'Programming',)

    group_1 = Group(group_name='1-MDA-7')
    group_2 = Group(group_name='1-MDA-9')

    session.add(group_1)
    session.add(group_2)

    for key, it in enumerate(lessons_names):
        lesson = Lesson(lesson_title=it)
        lesson.groups.append(group_1)
        if key % 2 == 0:
            lesson.groups.append(group_2)
        session.add(lesson)

    faker = Faker('ru_RU')
    group_list = (group_1, group_2)
    session.commit()

    for _ in range(50):
        full_name = faker.name().split(' ')
        age = faker.random.randint(16, 25)
        address = faker.address()
        group = faker.random.choice(group_list)
        student = Student(full_name, age, address, group.id)
        session.add(student)
    session.commit()
    session.close()
