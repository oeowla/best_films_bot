from __future__ import annotations
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""


# Ассоциативная таблица для связи фильмов и жанров
film_genre = Table(
    'film_genre',
    Base.metadata,
    Column('film_id', ForeignKey('films.id'), primary_key=True),
    Column('genre_id', ForeignKey('genres.id'), primary_key=True),
    comment='Связь между фильмами и жанрами'
)

#  Ассоциативная таблица для связи фильмов и категорий
film_category = Table(
    'film_category',
    Base.metadata,
    Column('film_id', ForeignKey('films.id'), primary_key=True),
    Column('category_id', ForeignKey('categories.id'), primary_key=True),
    comment='Связь между фильмами и категориями'
)


class Film(Base):
    """Модель фильма"""
    __tablename__ = 'films'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        comment='id фильма'
    )
    title: Mapped[str] = mapped_column(
        String,
        comment='Название фильма'
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=True,
        comment='Описание фильма'
    )

    # Связь с жанрами
    genres: Mapped[List['Genre']] = relationship(
        secondary=film_genre,
        back_populates='films',
        lazy='selectin',
        cascade='save-update, merge',
    )

    # Связь с категориями
    categories: Mapped[List['Category']] = relationship(
        secondary=film_category,
        back_populates='films',
        lazy='selectin',
        cascade='save-update, merge',
    )

    def __repr__(self) -> str:
        return f'Film(id={self.id}, title={self.title!r})'


class Genre(Base):
    """Модель жанра"""
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        comment='id жанра'
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        comment='Название жанра'
    )

    # Обратная связь с фильмами
    films: Mapped[List['Film']] = relationship(
        secondary=film_genre,
        back_populates='genres',
        lazy='selectin',
        cascade='save-update, merge',
    )

    def __repr__(self) -> str:
        return f'Genre(id={self.id}, name={self.name!r})'


class Category(Base):
    """Модель категории"""
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        comment='id категории'
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        comment='Название категории'
    )

    # Обратная связь с фильмами
    films: Mapped[List['Film']] = relationship(
        secondary=film_category,
        back_populates='categories',
        lazy='selectin',
        cascade='save-update, merge',
    )

    def __repr__(self) -> str:
        return f'Category(id={self.id}, name={self.name!r})'
