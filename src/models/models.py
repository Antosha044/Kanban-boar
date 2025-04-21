# Здесь модели таблиц из SQLAlchemy
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import uuid
from src.core.database import Base



class Users(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
