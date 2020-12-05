from data.availability import Availability  # pylint: disable = import-error
from data.park import Park  # pylint: disable = import-error
from data.region import Region  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
import datetime


def create_availability(start_date, end_date, park, availability):
    a = Availability()
    a.start_date = start_date
    a.end_date = end_date
    a.park = park
    a.availability = availability
    return a


def find_availability(start_date, end_date, park):
    session = db_session.create_session()

    availability = (
        session.query(Availability)
        .filter(Availability.start_date == start_date)
        .filter(Availability.end_date == end_date)
        .filter(Availability.park == park)
        .first()
    )

    session.close()

    return availability


def find_availability_info_for_date_range(start_date, end_date, park_list):
    session = db_session.create_session()

    available_parks = (
        session.query(Availability, Park, Region)
        .filter(Availability.start_date == start_date)
        .filter(Availability.end_date == end_date)
        .filter(Availability.availability == 1)
        .filter(Availability.park == Park.id)
        .filter(Availability.park.in_(park_list))
        .filter(Park.region == Region.id)
        .all()
    )

    session.close()
    
    return available_parks