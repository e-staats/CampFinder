import datetime
from services.search_services import deactivate_past_searches
import services.region_services as region_services
from services.url_services import format_date, set_up_url
from scraper.selenium_scraper import ParkScraper
import data.db_session as db_session
from data.search import Search

# pylint: disable = no-member

############################## KICK OFF FUNCTIONS ###################################
def scrape_searches(*args):
    all_searches = args[0]
    session = db_session.create_session()
    search_definition = {}
    print(f"scraping for searches at {datetime.datetime.now()}")

    if all_searches == True:
        search_list = session.query(Search).filter(Search.is_active == 1).all()
        if search_list == []:
            return "No searches in database"
        for search in search_list:
            search_definition = add_search_definition(search_definition, search)

    else:
        search = session.query(Search).filter(Search.is_active == 1).first()
        if search == None:
            return "No searches in database"
        search_definition = add_search_definition(search_definition, search)

    session.close()
    start_scraper(search_definition)
    cleanup_searches()


def scrape_searches_adhoc(start_date=None, end_date=None, region_id=None):
    if start_date == None or end_date == None:
        return "Problem starting scraper: Missing dates"
    if region_id == None:
        region_dict = region_services.define_regions()
    else:
        region_dict = {region_services.get_external_id(region_id): region_services.get_name_from_id(region_id)}
    search_definition = {}
    date_range = date_range_to_string(start_date, end_date)
    search_definition[date_range] = setup_info_dict(start_date, end_date, region_dict)

    scraper = ParkScraper(search_definition, True)
    scraper.parse()
    return scraper.get_results_dict()


############################ Helper Functions ####################################

def date_range_to_string(start_date, end_date) -> str:
    return format_date(start_date) + "-" + format_date(end_date)


def create_info_dict(start_date, end_date, search_time, region_dict):
    info = {}
    info["start_urls"] = {}
    for map_id in region_dict.keys():
        region_name = region_dict[map_id]
        info["start_urls"][region_name] = set_up_url(
            start_date, end_date, search_time, map_id
        )
    info["start_date"] = start_date
    info["end_date"] = end_date
    info["search_time"] = search_time
    return info


def setup_info_dict(start_date, end_date, region_dict) -> dict:
    search_time = datetime.datetime.now()
    return create_info_dict(
        start_date,
        end_date,
        search_time,
        region_dict,
    )


def start_scraper(search_definitions=None):
    if search_definitions == None:
        return "no start_urls provided - stopping"
    scraper = ParkScraper(search_definitions=search_definitions)
    scraper.parse()

def add_search_definition(search_definitions, search):
    date_range = date_range_to_string(search.start_date, search.end_date)
    # short circuit if we already have defs for this date range:
    if date_range in search_definitions.keys():
        return search_definitions
    region_dict = region_services.define_regions()
    search_definitions[date_range] = setup_info_dict(search.start_date, search.end_date, region_dict)
    return search_definitions


def cleanup_searches():
    deactivate_past_searches()
    return

