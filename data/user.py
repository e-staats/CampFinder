import sqlalchemy as sa
import datetime
from data.modelbase import SqlAlchemyBase # pylint: disable = import-error

class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    email = sa.Column(sa.String, index=True)
    hashed_pw = sa.Column(sa.String)
    status = sa.Column(sa.Integer)
    creation_date = sa.Column(sa.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"User {self.name}"