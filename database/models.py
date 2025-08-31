from __future__ import annotations
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""


film_genre = Table(
    'film_genre', Base.metadata,
    Column('film_id', ForeignKey('films.id'), primary_key=True),
    Column('genre_id', ForeignKey('genres.id'), primary_key=True),
)

film_category = Table(
    'film_category', Base.metadata,
    Column('film_id', ForeignKey('films.id'), primary_key=True),
    Column('category_id', ForeignKey('categories.id'), primary_key=True),
)

user_film = Table(
    'user_film', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('film_id', ForeignKey('films.id'), primary_key=True),
)

user_category = Table(
    'user_category', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('category_id', ForeignKey('categories.id'), primary_key=True),
)

user_genre = Table(
    'user_genre', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('genre_id', ForeignKey('genres.id'), primary_key=True),
)


class Film(Base):
    """Модель фильма"""
    __tablename__ = 'films'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True)

    title: Mapped[str] = mapped_column(
        String)

    description: Mapped[str] = mapped_column(
        String, nullable=True)

    genres: Mapped[List['Genre']] = relationship(
        secondary=film_genre,
        back_populates='films',
        lazy='selectin',
        cascade='save-update, merge',
    )

    categories: Mapped[List['Category']] = relationship(
        secondary=film_category,
        back_populates='films',
        lazy='selectin',
        cascade='save-update, merge',
    )

    users: Mapped[List['User']] = relationship(
        secondary=user_film,
        back_populates='films',
        lazy='select',
        cascade='save-update, merge',
    )

    def __repr__(self) -> str:
        return f'Film(id={self.id}, title={self.title!r})'


class Genre(Base):
    """Модель жанра"""
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)

    films: Mapped[List['Film']] = relationship(
        secondary=film_genre,
        back_populates='genres',
        lazy='selectin',
        cascade='save-update, merge',
    )

    users: Mapped[List['User']] = relationship(
        secondary=user_genre,
        back_populates='genres',
        lazy='select',
        cascade='save-update, merge',
    )

    def __repr__(self) -> str:
        return f'Genre(id={self.id}, name={self.name!r})'


class Category(Base):
    """Модель категории"""
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)

    films: Mapped[List['Film']] = relationship(
        secondary=film_category,
        back_populates='categories',
        lazy='selectin',
        cascade='save-update, merge',
    )

    users: Mapped[List['User']] = relationship(
        secondary=user_category,
        back_populates='categories',
        lazy='select',
        cascade='save-update, merge',
    )

    def __repr__(self) -> str:
        return f'Category(id={self.id}, name={self.name!r})'


class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True)

    telegram_id: Mapped[int] = mapped_column(
        Integer, unique=True)

    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)

    is_admin: Mapped[bool] = mapped_column(
        Boolean, default=False)

    films: Mapped[List['Film']] = relationship(
        secondary=user_film,
        back_populates='users',
        lazy='select',
        cascade='save-update, merge',
    )

    categories: Mapped[List['Category']] = relationship(
        secondary=user_category,
        back_populates='users',
        lazy='select',
        cascade='save-update, merge',
    )

    genres: Mapped[List['Genre']] = relationship(
        secondary=user_genre,
        back_populates='users',
        lazy='select',
        cascade='save-update, merge',
    )
