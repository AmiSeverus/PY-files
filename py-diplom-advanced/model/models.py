from email.policy import default
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
    user_id = sa.Column(sa.Integer, nullable=False)
    search_attr = sa.Column(sa.String(255), nullable=False)
    search_results = sa.Column(sa.Text, default=sa.null)
    searched_at = sa.Column(
        sa.TIMESTAMP,
        default=sa.func.now(),
        nullable=False)
