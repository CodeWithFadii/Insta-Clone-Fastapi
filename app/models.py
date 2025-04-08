from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship
from app.databse import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )

