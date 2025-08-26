import sqlalchemy
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
import datetime



Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.now(tz=datetime.timezone.utc), nullable=False)

    boards = relationship("Board", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
    

class Board(Base):
    __tablename__ = 'boards'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[DateTime] = mapped_column(default=datetime.datetime.now(tz=datetime.timezone.utc), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(default=datetime.datetime.now(tz=datetime.timezone.utc), onupdate=datetime.datetime.now(tz=datetime.timezone.utc), nullable=False)
    
    owner = relationship("User", back_populates="boards")
    lists = relationship("List", back_populates="board", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Board(name={self.name}, owner_id={self.owner_id})>"


class List(Base):
    __tablename__ = 'lists'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    board_id: Mapped[int]= mapped_column(ForeignKey('boards.id'))

    board = relationship("Board", back_populates="lists")
    cards = relationship("Card", back_populates="list", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<List(name={self.name}, board_id={self.board_id})>"
    

class Card(Base):
    __tablename__ = 'cards'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(index=True)
    list_id: Mapped[int] = mapped_column(ForeignKey('lists.id'))
    position: Mapped[int] = mapped_column(index=True)
    due_date: Mapped[DateTime] = mapped_column(index=True, nullable=True)

    list = relationship("List", back_populates="cards")

    def __repr__(self):
        return f"<Card(title={self.title}, list_id={self.list_id}, position={self.position})>"

