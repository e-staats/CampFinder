import sqlalchemy as sa
from data.modelbase import SqlAlchemyBase # pylint: disable = import-error


class Park(SqlAlchemyBase):
    __tablename__ = "parks"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, index=True)
    region = sa.Column(sa.Integer)
    #miles_from_madison = sa.Column(sa.Column) #will be good to add eventually

    def __repr__(self):
        return f"Park {self.name}"
