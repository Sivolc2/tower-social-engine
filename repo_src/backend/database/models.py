from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func # for server_default=func.now()
from repo_src.backend.database.connection import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now()) # server_default for initial creation

class User(Base):
    """
    User model representing a user profile in the Social OS system.
    This model is designed to be RAG-ready, with the wikiContent field
    serving as the primary source for future embedding and retrieval.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, unique=True, nullable=False, index=True)  # Stable, machine-readable identifier
    name = Column(String, nullable=False, index=True)
    bio = Column(Text, nullable=True)  # Short, one-line summary
    wiki_content = Column(Text, nullable=True)  # Rich, unstructured text for RAG system

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now()) 