import os
import sys
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
import data # pylint: disable = import-error
from data.result import Result # pylint: disable = import-error
from data.search import Search # pylint: disable = import-error
from data.availability import Availability # pylint: disable = import-error
from data.region import Region # pylint: disable = import-error
from data.user import User # pylint: disable = import-error
from datetime import datetime,timedelta
import data.constants # pylint: disable = import-error

ericsEmail = "eric.k.staats@gmail.com"
mikesEmail = "michael.v.cambria@gmail.com"
test_park_one = 1
test_park_two = 2

today = datetime.today()
tomorrow = today + timedelta(days=1)
overmorrow = tomorrow + timedelta(days=1)

def setup_all_test_data():
    db_file = os.path.join(os.path.dirname(__file__),'..','db','testdb.sqlite')
    data.db_session.global_init(db_file)
    session = data.db_session.factory()
    session.query(User).delete()
    session.query(Availability).delete()
    session.query(Search).delete()
    session.commit()

    add_data_to_session(test_users(), session)
    add_data_to_session(test_availabilities(), session)
    add_data_to_session(test_searches(), session)
    session.commit()
    session.close()

def add_data_to_session(data, session):
    for datum in data:
        session.add(datum)

def test_users():
    users_array = []
    test_array = [
        make_test_user("Beau", "michael.v.cambria@gmail.com"),
        make_test_user("Liam", "eric.k.staats@gmail.com")
    ]
    for test_user in test_array:
        user = User()
        user.name = test_user["name"]
        user.email = test_user["email"]
        user.status = data.constants.user_active_status
        user.creation_date = today
        users_array.append(user)
    return users_array

def make_test_user(name, email):
    return { "name": name, "email": email}

def test_availabilities():
    availabilities_array = []
    test_array = [
        make_test_availability(tomorrow, overmorrow, test_park_one, True),
        make_test_availability(tomorrow, overmorrow, test_park_two, False)
    ]
    for test_availability in test_array:
        availability = Availability()
        availability.start_date = test_availability["start_date"]
        availability.end_date = test_availability["end_date"]
        availability.park = test_availability["park"]
        availability.availability = test_availability["availability"]
        availabilities_array.append(availability)

    return availabilities_array

def make_test_availability(start_date, end_date, park, availability):
    return { "start_date": start_date, "end_date": end_date, "park": park, "availability": availability }

def test_searches():
     searches_array = []
     test_array = [
         make_test_search(tomorrow, overmorrow, None, "1,2"),
         make_test_search(tomorrow, overmorrow, None, "2")
     ]
     for test_search in test_array:
         search = Search()
         search.start_date = test_search["start_date"]
         search.end_date = test_search["end_date"]
         search.preferred_region = test_search["preferred_region"]
         search.parks = test_search["parks"]
         searches_array.append(search)

     return searches_array

def make_test_search(start_date, end_date, preferred_region, parks):
    return {"start_date": start_date, "end_date": end_date, "preferred_region": preferred_region, "parks": parks}  