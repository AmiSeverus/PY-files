from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa


base = declarative_base()


class matches_shown(base):
    __tablename__ = 'matches_shown'
    user_id = sa.Column(sa.Integer, primary_key=True)
    pair_id = sa.Column(sa.Integer, primary_key=True)


class search_results(base):
    __tablename__ = 'search_results'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer)
    search_attr = sa.Column(sa.String(255))
    search_results = sa.Column(sa.Text)