import scrapy
import os
import sys
import requests
from scrapy.crawler import CrawlerProcess
from parkscraper.parkscraper.spiders.parkspiders import ParkSpider
from urllib.parse import urlencode
import datetime

URL_BASE = "https://wisconsin.goingtocamp.com/create-booking/results?"
DATE_SUFFIX = "T00:00:00.000Z"

quandrant_defs = {
  -2147483604: "Northwest WI",
  -2147483603: "Southwest WI",
  -2147483602: "Northeast WI",
  -2147483601: "Southeast WI",
}

url_dict = {
'mapId': None,
'searchTabGroupId': 0,
'bookingCategoryId': 0,
'startDate': None,
'endDate': None,
'nights': None,
'isReserving': 'true',
'equipmentId': -32768,
'subEquipmentId': -32768,
'partySize': 1,
}

def format_date(date,suffix=DATE_SUFFIX):
  return str(date.isoformat())+suffix

def format_url(url_base, url_dict):
  url = urlencode(url_dict)
  url = url_base+url
  return url

def calculate_nights(date_range):
  nights=date_range[0]-date_range[1]
  return nights.days

def create_urls(url_base, url_dict, date_range, quadrant_defs):
  url_list = []
  url_dict['start_date']=format_date(date_range[0])
  url_dict['end_date']=format_date(date_range[1])
  url_dict['nights']=calculate_nights(date_range)
  for map_id in quadrant_defs.keys():
    url_dict['mapId']=map_id
    url_list.append(format_url(url_base,url_dict))
  return url_list

today=datetime.date.today()
tomorrow=today + datetime.timedelta(days=1)
date_range = (today,tomorrow)
url_list=create_urls(URL_BASE, url_dict, date_range, quandrant_defs)

if __name__ == "__main__":
  process = CrawlerProcess()
  process.crawl(ParkSpider, start_urls=url_list)
  process.start()