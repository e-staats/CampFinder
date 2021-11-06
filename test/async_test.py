import os
import sys

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
import services.map_services as map_services  # pylint: disable = import-error
from data.db_session import global_init  # pylint: disable = import-error
import global_test_setup  # pylint: disable = import-error
import testing_tools  # pylint: disable = import-error
import time
import secrets
import urllib.error
import urllib.parse
import asyncio
import aiohttp
from aiohttp import ClientSession
import json
import pprint
from icecream import ic

async def fetch_json(url: str, session: ClientSession, **kwargs) -> json:
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    return await resp.json()

async def api_call(url: str, session: ClientSession, **kwargs) -> dict:
    try:
        json = await fetch_json(url=url, session=session, **kwargs)
    except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError,) as e:
        print(f"oopsie")
        return {}
    else:
        ic(json)
        return json

async def main():
    distance_url = map_services.gmap_distance_matrix_API_url("53703")
    place_url = map_services.gmap_place_API_url("Governor Dodge State Park")
    ic(distance_url)
    ic(place_url)
    async with ClientSession() as session:
        await asyncio.gather(api_call(distance_url, session))
        await asyncio.gather(api_call(place_url, session))

if __name__ == "__main__":
    secrets.create_environment_variables()
    # global_test_setup.prep_db()
    # testing_tools.setup_all_test_data()
    before = time.perf_counter()
    asyncio.run(main())    
    after = time.perf_counter()
    print(f"{after - before:0.4f} seconds")

