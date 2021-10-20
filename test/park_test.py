import os
import sys
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
import services.park_services as park_services # pylint: disable = import-error
import services.region_services as region_services # pylint: disable = import-error
from data.db_session import global_init # pylint: disable = import-error
from icecream import ic

global_init(os.path.join(os.path.dirname(__file__),'..','db','testdb.sqlite'))
region_services.populate_regions()
park_services.populate_parks()
park = park_services.get_park_from_id(1)
park_services.park_to_dict(park)
ic(park.lat)