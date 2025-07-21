# models/user.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"