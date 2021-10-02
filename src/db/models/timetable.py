from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relation

from src.db.db_session import SqlAlchemyBase

days_to_timetable = Table('timetable_days_to_timetable', SqlAlchemyBase.metadata,
                          Column('day', Integer, ForeignKey('timetable_days.id')),
                          Column('timetable', Integer, ForeignKey('timetables.id')))


class Timetable(SqlAlchemyBase):
    __tablename__ = 'timetables'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, default='Расписание 11 класса')
    days = relation('TimetableDay', secondary='timetable_days_to_timetable', backref='timetables')

    def __str__(self):
        return self.name