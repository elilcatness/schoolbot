from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relation

from src.db.db_session import SqlAlchemyBase


class SubjectPosition(SqlAlchemyBase):
    __tablename__ = 'subject_positions'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    position = Column(Integer)
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    subject = relation('Subject')
    timetable_day_id = Column(Integer, ForeignKey('timetable_days.id'))
    timetable_day = relation('TimetableDay')