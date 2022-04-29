from curses import echo
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from model import models


class DB():

    def __init__(self):
        self.engine = create_engine(
            "postgresql+psycopg2://postgres:postgres@localhost/db_diploma_py_advanced",
            echo=True,
            encoding='utf8')
        models.base.metadata.create_all(self.engine)
        self.conn = sessionmaker(bind=self.engine)()

    def getConn(self):
        return self.conn
