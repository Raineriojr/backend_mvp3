from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from models import Base


class Friend(Base):
    __tablename__ = "friends"

    id = Column("friend_id", Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(70), nullable=True, unique=True)
    country = Column(String(25))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)

    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship('User', back_populates='friends')

    def __init__(
        self,
        name: str,
        email: str,
        country: str,
        user_id: int
    ):
        self.name = name
        self.email = email
        self.country = country
        self.user_id = user_id
