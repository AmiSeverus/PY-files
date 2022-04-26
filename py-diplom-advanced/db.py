import sqlalchemy

from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/db_diploma_py_advanced")

engine.connect()

class SearchResult():
    pass