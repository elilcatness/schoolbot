from sqlalchemy import Column, Integer, String

from src.db.db_session import SqlAlchemyBase


class Photo(SqlAlchemyBase):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    path = Column(String)

    @staticmethod
    def from_bytes(data, path):
        with open(path, 'wb') as img:
            img.write(data)
        return Photo(path=path)