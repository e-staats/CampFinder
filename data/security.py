import sqlalchemy as sa
import datetime
from data.modelbase import SqlAlchemyBase  # pylint: disable = import-error


class Security(SqlAlchemyBase):
    __tablename__ = "security"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    create_account = sa.Column(sa.Boolean)
    creation_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    is_active = sa.Column(sa.Integer, default=True)

    def __repr__(self):
        return f"Security Class {self.name}"