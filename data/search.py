import datetime
import sqlalchemy as sa
from data.modelbase import SqlAlchemyBase # pylint: disable = import-error


class Search(SqlAlchemyBase):
    __tablename__ = "searches"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    owner_id = sa.Column(sa.Integer)
    start_date = sa.Column(sa.Date)
    end_date = sa.Column(sa.Date)
    regions = sa.Column(sa.String)
    parks = sa.Column(sa.String)
    is_active = sa.Column(sa.Boolean, default=True)
    submit_instant = sa.Column(sa.DateTime, default=datetime.datetime.now)
    

    def __repr__(self):
        return f"Result {self.start_date} - {self.end_date}"
