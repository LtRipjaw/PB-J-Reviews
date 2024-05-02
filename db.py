from sqlalchemy import Table, Column, Integer, String, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from app import app

db = SQLAlchemy(app)
migrate = Migrate(app,db)

class users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Franchises(db.Model):
    __tablename__ = "franchises"

    id = Column('id', Integer, primary_key = True)
    name = Column('name', String, nullable=False)


class Developers(db.Model):
    __tablename__ = "developers"
    id = Column('id', Integer, primary_key = True)
    name = Column('name', String, nullable=False)
    location = Column('location', String)


class Directors(db.Model):
    __tablename__ = "directors"
    id = Column('id', Integer, primary_key = True),
    name = Column('name', String, nullable=False),
    age = Column('age', Integer)


class Moviess(db.Model):
    __tablename__ = "movies"
    id = Column('id', Integer, primary_key = True)
    title = Column('title', String, nullable=False)
    genre = Column('genre', String)
    director = Column('director', String, ForeignKey("directors.name"), nullable=False)
    franchise = Column('franchise', String, ForeignKey("franchises.name"))
    rating = Column('rating', Integer)


class Shows(db.Model):
    __tablename__ = "shows"
    id = Column('id', Integer, primary_key = True)
    title = Column('title', String, nullable=False)
    genre = Column('genre', String)
    director = Column('director', String, ForeignKey("directors.name"), nullable=False)
    franchise = Column('franchise', String, ForeignKey("franchises.name"))
    rating = Column('rating', Integer)


class Games(db.Model):
    __tablename__ = "games"
    id = Column('id', Integer, primary_key = True)
    title = Column('title', String, nullable=False)
    genre = Column('genre', String)
    developer = Column('developer', String, ForeignKey("developers.name"), nullable=False)
    franchise = Column('franchise', String, ForeignKey("franchises.name"))
    rating = Column('rating', Integer)