import sqlalchemy
from sqlalchemy import orm
from data.db_data.db_session import SqlAlchemyBase


class ImagePosts(SqlAlchemyBase):
    __tablename__ = "images"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    post_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    pos = sqlalchemy.Column(sqlalchemy.Integer)
    image = sqlalchemy.Column(sqlalchemy.BLOB)
