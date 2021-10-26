from icecream import ic
from data.park import Park  # pylint: disable = import-error
import services.park_services as park_services  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
from urllib.parse import urlencode
import os
import asyncio
import aiohttp
from aiohttp import ClientSession
import json
import pprint


def validate_zip_code(zip):
    if len(zip) != 5:
        return False

    if zip.isnumeric() == False:
        return False

    return True


def construct_API_call(url_base: str, url_info: dict) -> str:
    encoded = urlencode(url_info)
    url = url_base + "?" + encoded
    return url


def get_destinations(dest_arr) -> str:
    rtr_list = []
    i = 0
    for park in dest_arr:
        rtr_list.append("place_id:" + park.place_id)
    return "|".join(rtr_list)


def gmap_place_API_url(name: str) -> str:
    base = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    url_info = {
        "input": name,
        "inputtype": "textquery",
        "fields": "formatted_address,name,geometry,place_id",
        "key": os.environ["PLACE_API"],
    }
    url = construct_API_call(base, url_info)
    return url


def gmap_distance_matrix_API_url(origin: str, dest_arr: list) -> str:
    base = "https://maps.googleapis.com/maps/api/distancematrix/json"
    url_info = {
        "units": "imperial",
        "origins": origin,
        "destinations": get_destinations(dest_arr),
        "key": os.environ["DISTANCE_MATRIX_API"],
    }
    url = construct_API_call(base, url_info)
    return url


async def get_place_info_for_all_parks():
    """
    this will get the location, latitude, and longitude for all the parks in
    the database. It prints them out in a pipe delimited format to allow for
    manual resolution. The results can then be put into the park data CSV to
    cache them."""
    parks = park_services.get_all_parks()
    for park in parks:
        park_name = park.name + " State Park"
        place_url = gmap_place_API_url(park_name)
        async with ClientSession() as session:
            json = await asyncio.gather(api_call(place_url, session))
        data = json[0]
        if data["status"] != "OK":
            print(json)
            continue
        for candidate in data["candidates"]:
            output = []
            output.append(str(park.id))
            output.append(park.name)
            output.append(candidate["formatted_address"].replace(",", ""))
            output.append(str(candidate["geometry"]["location"]["lat"]))
            output.append(str(candidate["geometry"]["location"]["lng"]))
            output.append(candidate["place_id"])
            print("|".join(output))
    return


async def origin_to_all_parks(zip):
    results = {}
    parks = park_services.get_all_parks()
    arr_len = len(parks)
    max_requests = 25
    iterations = arr_len // max_requests + 1
    for i in range(iterations):
        slice_start = i * max_requests
        slice_end = (i + 1) * max_requests
        if slice_end >= len(parks):
            slice_end = len(parks) - 1
        url = gmap_distance_matrix_API_url(zip, parks[slice_start:slice_end])
        async with ClientSession() as session:
            json = await asyncio.gather(api_call(url, session))
        data = json[0]
        results = parse_distance_matrix(data, results, parks[slice_start:slice_end])
    return results


def parse_distance_matrix(data, results, parks) -> dict:
    updates = results
    for i in range(len(parks)):
        park = parks[i]
        status = data["rows"][0]["elements"][i]["status"]
        if status == "OK":
            time = data["rows"][0]["elements"][i]["duration"]["text"]
            distance = data["rows"][0]["elements"][i]["distance"]["text"]
        else:
            time = "Not driveable"
            distance = "Not driveable"
        updates[park.id] = {
            "name": park.name,
            "time": time,
            "distance": distance,
            "lng": park.lng,
            "lat": park.lat,
        }
    return updates

async def get_origin_place_data(zip: str):
    place_data = {}
    url = gmap_place_API_url(zip)
    async with ClientSession() as session:
        json = await asyncio.gather(api_call(url, session))
    data = json[0]
    try:
        candidate = data['candidates'][0]
    except:
        print("Places API failed to return a candidate")
        return {}
    place_data['id'] = 0
    place_data['isChecked'] = False
    place_data['name'] = zip
    place_data['lat'] = candidate["geometry"]["location"]["lat"]
    place_data['lng'] = candidate["geometry"]["location"]["lng"]
    return place_data

async def get_zip_distance_data(zip):
    return_dict = {}
    return_dict['origin'] = await get_origin_place_data(zip)
    return_dict['parks'] = await origin_to_all_parks(zip)
    return return_dict

async def fetch_json(url: str, session: ClientSession, **kwargs) -> json:
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    return await resp.json()


async def api_call(url: str, session: ClientSession, **kwargs) -> dict:
    try:
        json = await fetch_json(url=url, session=session, **kwargs)
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        print(f"oopsie")
        return {}
    else:
        return json
