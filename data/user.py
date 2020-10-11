import sqlalchemy as sa
from data.modelbase import SqlAlchemyBase # pylint: disable = import-error


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    def __repr__(self):
        return f"User {self.name}"