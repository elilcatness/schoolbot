from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relation

from src.db.db_session import SqlAlchemyBase


class Teacher(SqlAlchemyBase):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)
    subjects = relation('Subject')

    def __str__(self):
        return self.name