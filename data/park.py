import sqlalchemy as sa
from sqlalchemy.sql.schema import ForeignKey
from data.modelbase import SqlAlchemyBase # pylint: disable = import-error


class Park(SqlAlchemyBase):
    __tablename__ = "parks"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, index=True)
    region = sa.Column(sa.Integer, ForeignKey("regions.id"))
    external_id = sa.Column(sa.Integer, unique=True)
    address = sa.Column(sa.String)
    lat = sa.Column(sa.Float)
    lng = sa.Column(sa.Float)
    place_id = sa.Column(sa.String)

    def __repr__(self):
        return f"Park {self.name}"
