import datetime
import sqlalchemy
from sqlalchemy import orm
from data.db_data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    dataStart = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    news = orm.relationship("Posts", back_populates='user')
    profile = orm.relationship('ImagePosts')
