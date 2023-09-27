from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from models import Base


class User(Base):
    __tablename__ = "users"

    id = Column("user_id", Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(70), nullable=True, unique=True)
    password = Column(String(100))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)

    friends = relationship("Friend", back_populates="user")

    def __init__(
        self,
        name: str,
        email: str,
        password: str,
    ):
        self.name = name
        self.email = email
        self.password = password
