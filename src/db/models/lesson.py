import os.path
from sqlalchemy import Column, Integer, ForeignKey, Table, Date
from sqlalchemy.orm import relation

from src.db.db_session import SqlAlchemyBase
from src.db.models.homework import Homework
from src.db.models.photo import Photo
from src.utils import make_transliteration
from src.constants import PHOTO_DIR

photos_to_lesson = Table('photos_to_lesson', SqlAlchemyBase.metadata,
                         Column('photo', Integer, ForeignKey('photos.id')),
                         Column('lesson', Integer, ForeignKey('lessons.id')))


class Lesson(SqlAlchemyBase):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    date = Column(Date)
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    subject = relation('Subject', foreign_keys=subject_id)
    homework_id = Column(Integer, ForeignKey('homeworks.id'), nullable=True)
    homework = relation('Homework', foreign_keys=homework_id)
    photos = relation('Photo', secondary='photos_to_lesson', backref='lessons')

    def add_homework(self, description):
        self.homework = Homework(
            lesson_id=self.id, lesson=self,
            description=description)

    def process_photo(self, photo_bytes):
        path = os.path.join(
            PHOTO_DIR, f'{make_transliteration(self.subject.name.lower()).replace(" ", "-")}-'
                       f'{self.date.strftime("%d-%m-%Y")}-klass-{len(self.photos) + 1}.png')
        return Photo.from_bytes(photo_bytes, path)

    def __str__(self):
        return f'{self.subject.name}. {self.date.strftime("%d.%m.%Y")}.' \
               f'\nДомашнее задание: {self.homework.description if self.homework else "Нет"}'