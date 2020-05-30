import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

#...

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def test_year(input_year):
    if input_year.isdigit() and int(input_year)<=datetime.datetime.today().year:
        return True

def find_new(artist,album):
    # Находит запись в базе данных по заданному артисту и альбому
    session = connect_db()
    if session.query(Album).filter(Album.artist == artist, Album.album == album).first() == None:
        return True
    else:
        return False
