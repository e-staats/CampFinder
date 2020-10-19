import sqlalchemy as sa
from sqlalchemy.sql.schema import ForeignKey
from data.modelbase import SqlAlchemyBase # pylint: disable = import-error


class Park(SqlAlchemyBase):
    __tablename__ = "parks"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, index=True)
    region = sa.Column(sa.Integer, ForeignKey("regions.id"))
    #miles_from_madison = sa.Column(sa.Column) #will be good to add eventually

    def __repr__(self):
        return f"Park {self.name}"
