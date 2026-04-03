from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base

class DiaryEntry(Base):
    __tablename__ = "diary_entries"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title      = Column(String(200), nullable=False)
    content    = Column(Text, nullable=False)
    mood       = Column(String(20), default="보통")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)