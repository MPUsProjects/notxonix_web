import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class NotxonixData(SqlAlchemyBase):
    __tablename__ = 'gamedata'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)