from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.db import Base
from uuid import uuid4

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    stream_key = Column(String, unique=True, default=lambda: str(uuid4()))

    def __repr__(self):
        return f"<User id={self.id} email={self.email}, stream_key={self.stream_key}>"