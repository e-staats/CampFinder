import os
import sys

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
import data  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
from data.result import Result  # pylint: disable = import-error
from data.search import Search  # pylint: disable = import-error
from data.availability import Availability  # pylint: disable = import-error
from data.region import Region  # pylint: disable = import-error
from data.user import User  # pylint: disable = import-error
from datetime import datetime, timedelta
import data.constants  # pylint: disable = import-error
import services.region_services as region_services  # pylint: disable = import-error
import services.park_services as park_services  # pylint: disable = import-error


def prep_db():
    # delete and re-initialize the db from scratch:
    db_file = os.path.join(os.path.dirname(__file__), "..", "db", "testdb.sqlite")
    try:
        os.remove(db_file)
    except PermissionError:
        sys.exit("Close the database in DB Viewer first!")
    except:
        pass
    db_session.global_init(db_file)

    # add the constant data
    region_services.populate_regions()
    park_services.populate_parks()
