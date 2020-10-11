import os
import sys
import requests
from selenium_scraper import ParkScraper
from urllib.parse import urlencode
import datetime


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


def format_date(date, suffix):
    return str(date.isoformat()) + suffix


def format_url(url_base, url_setup):
    url = urlencode(url_setup)
    url = url_base + url
    return url


def calculate_nights(date_range):
    nights = date_range[1] - date_range[0]
    return nights.days


def create_urls(url_base, url_setup, date_range, search_time, quadrant_defs):
    suffix = define_date_suffix()
    url_setup["startDate"] = format_date(date_range[0], suffix)
    url_setup["endDate"] = format_date(date_range[1], suffix)
    url_setup["nights"] = calculate_nights(date_range)

    urls = {}
    for map_id in quadrant_defs.keys():
        url_setup["mapId"] = map_id
        region_name = quadrant_defs[map_id]
        urls[region_name] = (
            format_url(url_base, url_setup).replace("%3A", ":") + "&" + search_time
        )
    return urls


def get_start_date():
    # return datetime.date(2020, 10, 10)
    return datetime.date.today()


def get_end_date(start_date):
    return start_date + datetime.timedelta(days=1)


def setup_url_list():
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
    start = get_start_date()
    end = get_end_date(start)
    date_range = (start, end)
    search_time = (
        datetime.datetime.now()
        .astimezone()
        .strftime("%a %b %d %Y %H%M:%S GMT%z (%Z)")
        .replace(" ", "%20")
    )
    url_list = create_urls(url_base, url_setup, date_range, search_time, quadrant_defs)
    return url_list


def start_scraper(start_urls=None):
    if start_urls == None:
        return "no start_urls provided - stopping"
    scraper = ParkScraper(start_urls=start_urls)
    scraper.parse()


if __name__ == "__main__":
    start_urls = setup_url_list()
    start_scraper(start_urls=start_urls)
