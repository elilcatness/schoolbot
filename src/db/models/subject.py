from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relation

from src.db.db_session import SqlAlchemyBase


class Subject(SqlAlchemyBase):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=True)
    teacher = relation('Teacher', foreign_keys=teacher_id, back_populates='subjects')

    def __str__(self):
        return f'Предмет: {self.name}. Учитель: {self.teacher if self.teacher else "Нет"}'