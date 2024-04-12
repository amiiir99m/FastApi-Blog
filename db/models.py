from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from .engine import Base


class User(Base):
    __tablename__ ="users"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)


class Post(Base):
    __tablename__="posts"

    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]= mapped_column()
    author: Mapped[str] = mapped_column(ForeignKey("users.username"))
    image_url: Mapped[str] = mapped_column()
    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)


