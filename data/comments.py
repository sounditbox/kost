from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer

from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String)
    created_date = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(ForeignKey("users.id"))
    user = relationship('User', back_populates="comments")
    article_id = Column(ForeignKey("article.id"))
    article = relationship('Article', back_populates="comments")
