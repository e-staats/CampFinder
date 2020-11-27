import os
import sys
from datetime import datetime, timedelta

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
import data.db_session as db_session  # pylint: disable = import-error
import data.constants as constants  # pylint: disable = import-error
import services.availability_services as avail_services  # pylint: disable = import-error
import services.search_services as search_services  # pylint: disable = import-error
import services.user_services as user_services  # pylint: disable = import-error
import services.result_services as result_services  # pylint: disable = import-error

ericsEmail = "eric.k.staats@gmail.com"
mikesEmail = "michael.v.cambria@gmail.com"
test_park_one = 1
test_park_two = 2

today = datetime.today()
tomorrow = today + timedelta(days=1)
overmorrow = tomorrow + timedelta(days=1)
overovermorrow = overmorrow + timedelta(days=1)
yesterday = today - timedelta(days=1)


def setup_all_test_data():
    session = db_session.create_session()
    add_data_to_session(test_users(), session)
    add_data_to_session(test_availabilities(), session)
    add_data_to_session(test_results(), session)
    add_data_to_session(test_searches(), session)
    session.commit()
    session.close()


def add_data_to_session(data, session):
    for datum in data:
        session.add(datum)


def test_users():
    return [
        user_services.create_user("Beau", "michael.v.cambria@gmail.com", "abc", 1),
        user_services.create_user("Liam", "eric.k.staats@gmail.com", "def", 2),
    ]


def test_availabilities():
    return [
        avail_services.create_availability(tomorrow, overmorrow, test_park_one, False),
        avail_services.create_availability(tomorrow, overmorrow, test_park_two, False),
        avail_services.create_availability(
            overmorrow, overovermorrow, test_park_one, True
        ),
        avail_services.create_availability(
            overmorrow, overovermorrow, test_park_two, True
        ),
    ]


def test_results():
    return [
        result_services.create_result(tomorrow, overmorrow, datetime.now()),
        result_services.create_result(overmorrow, overovermorrow, datetime.now()),
    ]


def test_searches():
    return [
        search_services.create_search(1, tomorrow, overmorrow, None, "1,2", True),
        search_services.create_search(1, tomorrow, overmorrow, None, "1", False),
        search_services.create_search(
            2, overmorrow, overovermorrow, None, "1,2", False
        ),
        search_services.create_search(2, tomorrow, overmorrow, None, "1,2", True),
        search_services.create_search(2, overmorrow, overovermorrow, None, "2", True),
        search_services.create_search(2, overmorrow, overovermorrow, None, "2", True),
        search_services.create_search(2, yesterday, today, None, "2", True),
    ]
