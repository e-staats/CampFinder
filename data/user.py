from collections import defaultdict
import sqlalchemy as sa
import datetime
from data.modelbase import SqlAlchemyBase  # pylint: disable = import-error
from sqlalchemy.sql.schema import ForeignKey

class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    email = sa.Column(sa.String, index=True, unique=True)
    phone_number = sa.Column(sa.String)
    hashed_pw = sa.Column(sa.String)
    creation_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    is_active = sa.Column(sa.Integer, default=True)
    security_class = sa.Column(sa.Integer, ForeignKey("security.id"))
    send_emails = sa.Column(sa.Boolean, default=True)
    send_texts = sa.Column(sa.Boolean, default=False)
    
    def __repr__(self):
        return f"User {self.name}"