import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, DateTime,Float
from sqlalchemy.dialects.postgresql import UUID, ARRAY, TSVECTOR, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from core.base_class import Base
from db_models.db_serializer import TextPickleType




class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username=Column(String)
    email = Column(String)
    hashed_password = Column(String)
    verified = Column(Boolean, nullable=False, server_default='False')
    is_active = Column(Boolean, default=True)

class HashedToken(Base):
    __tablename__ = "hashed_tokens"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    hashed_token = Column(String, index=True)
