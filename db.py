from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

engine = create_engine('sqlite:///pbjreviews.db', echo=True)
meta = MetaData()



franchises = Table(
    'franchises', meta,
    Column('id', Integer, primary_key = True),
    Column('name', String)
)

developers = Table(
    'developers', meta,
    Column('id', Integer, primary_key = True),
    Column('name', String),
    Column('location', String),
)

directors = Table(
    'directors', meta,
    Column('id', Integer, primary_key = True),
    Column('name', String),
    Column('age', Integer)
)

movies = Table(
    'movies', meta,
    Column('id', Integer, primary_key = True),
    Column('title', String),
    Column('genre', String),
    Column('director', String, ForeignKey(directors.name)),
    Column('franchise', String, ForeignKey(franchises.name)),
    Column('rating', Integer)
)

shows = Table(
    'shows', meta,
    Column('id', Integer, primary_key = True),
    Column('title', String),
    Column('genre', String),
    Column('director', String, ForeignKey(directors.name)),
    Column('franchise', String, ForeignKey(franchises.name)),
    Column('rating', Integer)
)

games = Table(
    'games', meta,
    Column('id', Integer, primary_key = True),
    Column('title', String),
    Column('genre', String),
    Column('developer', String, ForeignKey(developers.name)),
    Column('franchise', String, ForeignKey(franchises.name)),
    Column('rating', Integer)
)

meta.create_all(engine)