from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relation

from src.db.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    role = Column(String, default='user')
    chosen_timetable_id = Column(Integer, ForeignKey('timetables.id'))
    chosen_timetable = relation('Timetable', foreign_keys=chosen_timetable_id)