from collections import defaultdict
import sqlalchemy as sa
import datetime
import uuid
from data.modelbase import SqlAlchemyBase  # pylint: disable = import-error
from sqlalchemy.sql.schema import ForeignKey

class User(SqlAlchemyBase):
    __tablename__ = "users"

    def get_id(self):
        return uuid.uuid4().hex

    id = sa.Column(sa.String, primary_key=True, default=get_id)
    name = sa.Column(sa.String)
    email = sa.Column(sa.String, index=True, unique=True)
    phone_number = sa.Column(sa.String)
    hashed_pw = sa.Column(sa.String)
    creation_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    is_active = sa.Column(sa.Integer, default=False)
    security_class = sa.Column(sa.Integer, ForeignKey("security.id"))
    send_emails = sa.Column(sa.Boolean, default=True)
    send_texts = sa.Column(sa.Boolean, default=False)
    
    def __repr__(self):
        return f"User {self.name}"
