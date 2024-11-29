from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)

    # one to many connection
    notes = relationship('Note', back_populates='user', cascade='all, delete')

    def __str__(self):
        return f"<User(id={self.id}, username={self.username})>"
