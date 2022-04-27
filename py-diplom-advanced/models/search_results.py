import sqlalchemy as sa
from base import base

class search_results(base):
    __tablename__ = 'search_results'
    user_id = sa.Column(sa.Integer)
    search_attr = sa.Column(sa.String(255))
    search_results = sa.Column(sa.Text)