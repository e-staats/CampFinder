import sqlalchemy as sa
from data.modelbase import SqlAlchemyBase # pylint: disable = import-error


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    email = sa.Column(sa.String)
    hashed_pw = sa.Column(sa.String)
    status = sa.Column(sa.Integer)
    creation_date = sa.Column(sa.DateTime)

    def __repr__(self):
        return f"User {self.name}"