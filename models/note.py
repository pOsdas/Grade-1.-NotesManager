from sqlalchemy import (
    Column, Integer, String,
    ForeignKey, DateTime, event,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from models.base import Base


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    issue_date = Column(DateTime, nullable=True)
    comment = Column(String, nullable=True)

    # one to many connection
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='notes')

    def __repr__(self):
        return (
            f"<Note(id={self.id}, title={self.title}>, content={self.content}, status={self.status}, "
            f"created_date={self.created_date}, issue_date={self.issue_date}, "
            f"comment={self.comment}, user_id={self.user_id})>"
        )
