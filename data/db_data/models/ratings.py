import sqlalchemy
from sqlalchemy import orm
from data.db_data.db_session import SqlAlchemyBase


class Ratings(SqlAlchemyBase):
    __tablename__ = 'ratings'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    post_id = sqlalchemy.Column(
        sqlalchemy.String, sqlalchemy.ForeignKey("posts.id"), nullable=False)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)

    post = orm.relationship("Posts")
    user = orm.relationship("User")
