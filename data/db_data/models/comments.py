import sqlalchemy
from sqlalchemy import orm
from data.db_data.db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    post_id = sqlalchemy.Column(
        sqlalchemy.String, sqlalchemy.ForeignKey("posts.id"), nullable=False)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=sqlalchemy.func.now())

    post = orm.relationship("Posts", back_populates="comments")
    user = orm.relationship("User")
