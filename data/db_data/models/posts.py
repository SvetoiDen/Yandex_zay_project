import datetime
import sqlalchemy
from sqlalchemy import orm
from data.db_data.db_session import SqlAlchemyBase


class Posts(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, nullable=True)
    userId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    namePost = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    descPost = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rating = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user = orm.relationship('User')
    comments = orm.relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan")