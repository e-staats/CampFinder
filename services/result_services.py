from data.result import Result # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
import datetime 

def create_result(start_date, end_date, retrieval_time):
    r = Result()
    r.start_date=start_date
    r.end_date=end_date
    r.retrieval_time=retrieval_time
    return r

def find_result(start_date, end_date, session=None):
    if session == None:
        session = db_session.create_session()

    result = (
        session.query(Result)
        .filter(Result.start_date == start_date)
        .filter(Result.end_date == end_date)
        .first()
    )

    return result

def validate_datetime():
    pass