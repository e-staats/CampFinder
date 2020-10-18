import os
import sys
import requests
from selenium_scraper import ParkScraper
from urllib.parse import urlencode
import datetime
import data.db_session as db_session
from data.search import Search

# pylint: disable = no-member


def define_date_suffix():
    return "T00:00:00.000Z"


def define_url_base():
    return "https://wisconsin.goingtocamp.com/create-booking/results?"


def define_regions():
    return {
        -2147483604: "Northwest WI",
        -2147483603: "Southwest WI",
        -2147483602: "Northeast WI",
        -2147483601: "Southeast WI",
    }


def format_date(date, suffix="") -> str:
    return str(date.isoformat()) + suffix


def format_url(url_base, url_setup, search_time):
    url = urlencode(url_setup)
    url = url_base + url + "&" + format_searchtime(search_time)
    return url.replace("%3A", ":")


def format_searchtime(search_time):
    return (
        search_time.astimezone()
        .strftime("%a %b %d %Y %H%M:%S GMT%z (%Z)")
        .replace(" ", "%20")
    )


def calculate_nights(date_range):
    nights = date_range[1] - date_range[0]
    return nights.days


def date_range_to_string(start_date, end_date) -> str:
    return format_date(start_date) + "-" + format_date(end_date)


def create_info_dict(
    url_base, url_setup, start_date, end_date, search_time, quadrant_defs
):
    suffix = define_date_suffix()
    url_setup["startDate"] = format_date(start_date, suffix=suffix)
    url_setup["endDate"] = format_date(end_date, suffix=suffix)
    url_setup["nights"] = calculate_nights((start_date, end_date))

    info = {}
    info["start_urls"] = {}
    for map_id in quadrant_defs.keys():
        url_setup["mapId"] = map_id
        region_name = quadrant_defs[map_id]
        info["start_urls"][region_name] = format_url(url_base, url_setup, search_time)
    info["start_date"] = start_date
    info["end_date"] = end_date
    info["search_time"] = search_time
    return info


def setup_info_dict(search: Search) -> dict:
    if search.id == None:
        return "Invalid Search object"

    url_setup = {
        "mapId": None,
        "searchTabGroupId": 0,
        "bookingCategoryId": 0,
        "startDate": None,
        "endDate": None,
        "nights": None,
        "isReserving": "true",
        "equipmentId": -32768,
        "subEquipmentId": -32768,
        "partySize": 1,
    }

    quadrant_defs = define_regions()
    url_base = define_url_base()
    search_time = datetime.datetime.now()
    return create_info_dict(
        url_base,
        url_setup,
        search.start_date,
        search.end_date,
        search_time,
        quadrant_defs,
    )


def start_scraper(search_definitions=None):
    if search_definitions == None:
        return "no start_urls provided - stopping"
    scraper = ParkScraper(search_definitions=search_definitions)
    scraper.parse()


def scrape_searches(all_searches=False):
    session = db_session.create_session()
    search_definition = {}

    if all_searches == False:
        search = session.query(Search).filter(Search.is_active == 1).first()
        if search == None:
            return "No searches in database"
        search_definition = add_search_definition(search_definition, search)

    if all_searches == True:
        search_list = session.query(Search).filter(Search.is_active == 1).all()
        if search_list == []:
            return "No searches in database"
        for search in search_list:
            search_definition = add_search_definition(search_definition, search)

    session.close()

    start_scraper(search_definition)

def add_search_definition(search_definitions, search):
    date_range = date_range_to_string(search.start_date, search.end_date)
    search_definitions[date_range] = setup_info_dict(search)
    return search_definitions


if __name__ == "__main__":
    print(
        "Don't run directly; run test/scraper_tests.py if you want to test the scraper"
    )
