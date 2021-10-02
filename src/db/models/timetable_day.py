from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relation

from src.db.db_session import SqlAlchemyBase
from src.constants import TIMINGS

positions_to_timetable_day = Table('positions_to_timetable_day', SqlAlchemyBase.metadata,
                                   Column('position', Integer, ForeignKey('subject_positions.id')),
                                   Column('timetable_day', Integer, ForeignKey('timetable_days.id')))


class TimetableDay(SqlAlchemyBase):
    __tablename__ = 'timetable_days'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    weekday = Column(String, unique=True)
    timetable_id = Column(Integer, ForeignKey('timetables.id'))
    timetable = relation('Timetable', back_populates='days')
    positions = relation('SubjectPosition', secondary='positions_to_timetable_day',
                         backref='timetable_days')

    def __str__(self):
        return f'{self.weekday}\n%s' % '\n'.join(
            [f'{pos.subject.name}. {TIMINGS[pos.position - 1] if pos.position <= len(TIMINGS) else "Вне расписания"}'
             for pos in sorted(self.positions, key=lambda pos: pos.position)])
