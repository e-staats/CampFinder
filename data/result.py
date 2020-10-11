import sqlalchemy as sa
from data.modelbase import SqlAlchemyBase # pylint: disable = import-error


class Result(SqlAlchemyBase):
    __tablename__ = "results"

    start_date = sa.Column(sa.Date, primary_key=True)
    end_date = sa.Column(sa.Date, primary_key=True)
    retrieval_time = sa.Column(sa.DateTime)

    def __repr__(self):
        return f"Result {self.start_date} - {self.end_date}"
