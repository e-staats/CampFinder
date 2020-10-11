import sqlalchemy as sa
from data.modelbase import SqlAlchemyBase # pylint: disable = import-error


class Query(SqlAlchemyBase):
    __tablename__ = "queries"

    id = sa.Column(sa.Integer, primary_key=True)
    start_date = sa.Column(sa.Date)
    end_date = sa.Column(sa.Date)
    preferred_region = sa.Column(sa.Date)
    end_date = sa.Column(sa.Date)
    retrieval_time = sa.Column(sa.DateTime)
    park = sa.Column(sa.Boolean)

    def __repr__(self):
        return f"Result {self.start_date} - {self.end_date}"
