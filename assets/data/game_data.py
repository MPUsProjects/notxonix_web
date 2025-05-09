import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class NotxonixData(SqlAlchemyBase):
    __tablename__ = 'gamedata'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True)
    LB = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    WB = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    MainB = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    Money = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    MexB = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    Skin = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    ShrekB = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    Main = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    Loki = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    Warrior = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    Mexicanes = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    Shrek = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    SkinCount = sqlalchemy.Column(sqlalchemy.String, nullable=False)