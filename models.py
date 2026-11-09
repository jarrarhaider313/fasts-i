from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey
from database import Base

class user(Base):
    __tablename__ = "user"

    id:Mapped[int]=mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(unique=True)
    password : Mapped[str] = mapped_column(nullable=False)

class Task(Base):
    __tablename__ = "Task"

    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(unique=True)
    description : Mapped[str] = mapped_column()
    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"))

