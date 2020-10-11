import sqlalchemy as sa
from data.modelbase import SqlAlchemyBase # pylint: disable = import-error


class Region(SqlAlchemyBase):
    __tablename__ = "regions"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)

    def __repr__(self):
        return f"Region {self.name}"
