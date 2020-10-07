import scrapy
import os
import sys
import requests
from scrapy.crawler import CrawlerProcess
from parkscraper.parkscraper.spiders.parkspiders import ParkSpider
from urllib.parse import urlencode
import datetime

def define_date_suffix():
  return "T00:00:00.000Z"

def define_url_base():
  return "https://wisconsin.goingtocamp.com/create-booking/results?"

def format_date(date, suffix):
    return str(date.isoformat()) + suffix


def format_url(url_base, url_dict):
    url = urlencode(url_dict)
    url = url_base + url
    return url


def calculate_nights(date_range):
    nights = date_range[1] - date_range[0]
    return nights.days


def create_urls(url_base, url_dict, date_range, search_time, quadrant_defs):
    suffix=define_date_suffix()
    url_list = []
    url_dict["startDate"] = format_date(date_range[0],suffix)
    url_dict["endDate"] = format_date(date_range[1],suffix)
    url_dict["nights"] = calculate_nights(date_range)
    for map_id in quadrant_defs.keys():
        url_dict["mapId"] = map_id
        url_list.append(
            format_url(url_base, url_dict).replace("%3A", ":") + "&" + search_time
        )
    return url_list


def setup_url_list():
    url_dict = {
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

    quadrant_defs = {
        -2147483604: "Northwest WI",
        -2147483603: "Southwest WI",
        -2147483602: "Northeast WI",
        -2147483601: "Southeast WI",
    }

    url_base=define_url_base()
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    date_range = (today, tomorrow)
    search_time = (
        datetime.datetime.now()
        .astimezone()
        .strftime("%a %b %d %Y %H%M:%S GMT%z (%Z)")
        .replace(" ", "%20")
    )
    url_list = create_urls(url_base, url_dict, date_range, search_time, quadrant_defs)
    return url_list


def start_scraper(start_urls):
    process = CrawlerProcess()
    process.crawl(ParkSpider, start_urls=start_urls)
    process.start()

def doodle():
  print("doogle goodle")

if __name__ == "__main__":
    start_urls = setup_url_list()
    start_scraper(start_urls)
