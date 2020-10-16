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
import datetime

ericsEmail = "eric.k.staats@gmail.com"
mikesEmail = "michael.v.cambria@gmail.com"

def setup_all_test_data():
    db_file = os.path.join(os.path.dirname(__file__),'..','db','testdb.sqlite')
    data.db_session.global_init(db_file)
    session = data.db_session.factory()
    session.query(User).delete()
    session.query(Availability).delete()
    session.query(Search).delete()
    session.commit()

    setup_test_users()

def setup_test_users():
    session = data.db_session.factory()
    for user in test_users():
        session.add(user)
    session.commit()

def test_users():
    test_array = []
    test_dictionary = {
        "names": ["Beau", "Liam"],
        "emails": ["michael.v.cambria@gmail.com", "eric.k.staats@gmail.com"]
    }
    for i in range(len(test_dictionary["names"])):
        user = User()
        user.name = test_dictionary["names"][i]
        user.email = test_dictionary["emails"][i]
        user.status = 1
        user.creation_date = datetime.datetime.now()
        test_array.append(user)
    return test_array
