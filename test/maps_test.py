import os
import sys

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
import services.map_services as map_services  # pylint: disable = import-error
import services.park_services as park_services  # pylint: disable = import-error
from data.db_session import global_init  # pylint: disable = import-error
import global_test_setup  # pylint: disable = import-error
import testing_tools  # pylint: disable = import-error
import time
import secrets
from icecream import ic
import asyncio

if __name__ == "__main__":
    secrets.create_environment_variables()
    global_test_setup.prep_db()
    testing_tools.setup_all_test_data()
    before = time.perf_counter()
    # ic(map_services.gmap_place_API_url("Governor Dodge State Park"))
    ic(asyncio.run(map_services.origin_to_all_parks("53703")))
    after = time.perf_counter()
    print(f"{after - before:0.4f} seconds")
