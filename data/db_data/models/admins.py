import sqlalchemy
from sqlalchemy import orm
from data.db_data.db_session import SqlAlchemyBase


class Admin(SqlAlchemyBase):
    __tablename__ = "admins"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True)
    # 3 = Суперадмин, 2 = Модератор, 1 = Оператор
    level = sqlalchemy.Column(sqlalchemy.Integer)
