from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
