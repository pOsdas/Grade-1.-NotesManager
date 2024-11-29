from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base

DATABASE_URL = 'sqlite:///notes_manager.db'

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def init_db():
    Base.metadata.create_all(bind=engine)
