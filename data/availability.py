import sqlalchemy as sa
from data.modelbase import SqlAlchemyBase # pylint: disable = import-error
from sqlalchemy import ForeignKey


class Availability(SqlAlchemyBase):
    __tablename__ = "availabilities"

    start_date = sa.Column(sa.Date, primary_key=True)
    end_date = sa.Column(sa.Date, primary_key=True)
    park = sa.Column(sa.Integer, ForeignKey("parks.id"), primary_key = True)
    availability = sa.Column(sa.Boolean)

    def __repr__(self):
        return f"Availability {self.start_date} - {self.end_date}"
