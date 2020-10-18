from data.availability import Availability  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
import datetime


def create_availability(start_date, end_date, park, availability):
    a = Availability()
    a.start_date = start_date
    a.end_date = end_date
    a.park = park
    a.availability = availability
    return a


def find_availability(start_date, end_date, park, session=None):
    if session == None:
        session = db_session.create_session()

    availability = (
        session.query(Availability)
        .filter(Availability.start_date == start_date)
        .filter(Availability.end_date == end_date)
        .filter(Availability.park == park)
        .first()
    )

    return availability