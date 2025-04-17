import uuid
from sqlalchemy import UUID, Column, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)

    user_name = Column(String, nullable=True, unique=True)
    profile_img = Column(String, nullable=True)

    followers = Column(Integer, nullable=True, server_default="0")
    followings = Column(Integer, nullable=True, server_default="0")
    posts = Column(Integer, nullable=True, server_default="0")

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
