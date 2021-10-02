import os.path

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relation

from src.constants import PHOTO_DIR
from src.db.db_session import SqlAlchemyBase
from src.db.models.photo import Photo
from src.utils import make_transliteration

photos_to_homework = Table('photos_to_homework', SqlAlchemyBase.metadata,
                           Column('photo', Integer, ForeignKey('photos.id')),
                           Column('homework', Integer, ForeignKey('homeworks.id')))


class Homework(SqlAlchemyBase):
    __tablename__ = 'homeworks'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    lesson = relation('Lesson', foreign_keys=lesson_id)
    description = Column(String)
    photos = relation('Photo', secondary='photos_to_homework', backref='homeworks')

    def process_photo(self, photo_bytes):
        path = os.path.join(
            PHOTO_DIR, f'{make_transliteration(self.lesson.subject.name.lower()).replace(" ", "-")}-'
                       f'{self.lesson.date.strftime("%d-%m-%Y")}-dz-{len(self.photos) + 1}.png')
        return Photo.from_bytes(photo_bytes, path)