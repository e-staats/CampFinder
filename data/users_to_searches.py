import sqlalchemy as sa
import datetime
from data.modelbase import SqlAlchemyBase # pylint: disable = import-error

class UserToSearch(SqlAlchemyBase):
    __tablename__ = "users_to_searches"

    user_id = sa.Column(sa.Integer, primary_key=True)
    search_id = sa.Column(sa.Integer, primary_key=True)