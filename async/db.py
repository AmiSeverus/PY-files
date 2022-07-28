from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func, Text, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import atexit

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/flask')
Base = declarative_base()
Session = sessionmaker(bind=engine)
atexit.register(lambda: engine.dispose())

class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birth_year = Column(String, nullable=True)
    eye_color = Column(String, nullable=True)
    films = Column(Text, nullable=False)
    gender = Column(String, nullable=True)
    hair_color = Column(String, nullable=True)
    height = Column(Float, nullable=True)
    homeworld = Column(String, nullable=False)
    mass = Column(Float, nullable=True)
    skin_color = Column(String, nullable=True)
    species = Column(Text, nullable=True)
    starships = Column(Text, nullable=True) 
    vehicles = Column(Text, nullable=True)

Base.metadata.create_all(engine)