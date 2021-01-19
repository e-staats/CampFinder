from urllib.parse import urlencode

def set_up_url(start_date, end_date, search_time, map_id):
    url_base = define_url_base()
    url_setup = def_url_setup()
    suffix = define_date_suffix()
    url_setup["startDate"] = format_date(start_date, suffix=suffix)
    url_setup["endDate"] = format_date(end_date, suffix=suffix)
    url_setup["nights"] = calculate_nights((start_date, end_date))
    url_setup["mapId"] = map_id
    return format_url(url_base, url_setup, search_time)

def def_url_setup():
    return {
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

def calculate_nights(date_range):
    nights = date_range[1] - date_range[0]
    return nights.days

def format_date(date, suffix="") -> str:
    return str(date.isoformat()) + suffix


def format_url(url_base, url_setup, search_time):
    url = urlencode(url_setup)
    url = url_base + url + "&" + format_searchtime(search_time)
    return url.replace("%3A", ":")

def define_date_suffix():
    return "T00:00:00.000Z"


def define_url_base():
    return "https://wisconsin.goingtocamp.com/create-booking/results?"


def format_searchtime(search_time):
    return (
        search_time.astimezone()
        .strftime("%a %b %d %Y %H%M:%S GMT%z (%Z)")
        .replace(" ", "%20")
    )




