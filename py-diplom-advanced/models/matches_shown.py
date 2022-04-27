import sqlalchemy as sa
from base import base

class matches_shown(base):
    __tablename__ = 'matches_shown'
    user_id = sa.Column(sa.Integer, primary_key=True)
    pair_id = sa.Column(sa.Integer, primary_key=True)