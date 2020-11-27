from data.search import Search  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
import services.user_services as user_services  # pylint: disable = import-error
import services.park_services as park_services  # pylint: disable = import-error
import services.region_services as region_services  # pylint: disable = import-error
import datetime


def create_search(owner_id, start_date, end_date, regions, parks, is_active):
    s = Search()
    s.owner_id = owner_id
    s.start_date = start_date
    s.end_date = end_date
    s.regions = regions
    s.parks = parks
    s.is_active = is_active

    return s


def add_search(search):
    session = db_session.create_session()
    session.add(search)
    session.commit()
    session.close()

    return True


def find_search_by_id(search_id):
    session = db_session.create_session()
    search = (
        session.query(Search)
        .filter(Search.id == search_id)
        .first()
    )
    session.close()

    return search


def find_active_searches():
    session = db_session.create_session()
    searches = session.query(Search).filter(Search.is_active == 1).all()
    session.close()

    return searches


def find_all_searches_for_user(user_id):
    session = db_session.create_session()
    searches = session.query(Search).filter(Search.owner_id == user_id).all()
    session.close()

    return searches


def find_users_interested_in_search(search_id):
    session = db_session.create_session()
    user_ids = session.query(Search.owner_id).filter(Search.id == search_id).all()
    user_ids = [user_id for user_id, in user_ids]
    users = [user_services.find_user_by_id(user_id) for user_id in user_ids]
    session.close()

    return users


def deserialize_park_list(parks):
    return [int(p_id) for p_id in parks.split(",") if p_id != '']


def deserialize_region_list(regions):
    return [int(r_id) for r_id in regions.split(",") if r_id != '']


def convert_to_dict(search):
    search_dict = search.__dict__
    search_dict.pop('_sa_instance_state',None)
    search_dict = format_dict_dates(search_dict)
    search_dict = format_dict_parks_and_regions(search_dict)
    return search_dict


def format_dict_dates(search_dict):
    for key, value in search_dict.items():
        if isinstance(value, datetime.date):
            search_dict[key] = value.strftime("%a %m/%d/%y")
        if isinstance(value, datetime.datetime):
            search_dict[key] = value.strftime("%a %m/%d/%y %I:%M %p")
    return search_dict


def format_dict_parks_and_regions(search_dict):
    search_dict["regions"] = deserialize_region_list(search_dict["regions"])
    search_dict["parks"] = deserialize_park_list(search_dict["parks"])
    search_dict["parks"] = compress_parks_to_regions(
        search_dict["parks"], search_dict["regions"]
    )
    search_dict["park_names"] = [
        park_services.get_name_from_id(park_id) for park_id in search_dict["parks"]
    ]
    search_dict["region_names"] = [
        region_services.get_name_from_id(region_id)
        for region_id in search_dict["regions"]
    ]
    return search_dict


def compress_parks_to_regions(parks, regions):
    if regions == "":
        return parks

    new_park_list = parks.copy()
    for region_id in regions:
        for park_id in parks:
            park = park_services.get_park_from_id(park_id)
            if park == False:
                continue
            if park.region == region_id:
                new_park_list.remove(park_id)
    return new_park_list


def deactivate_past_searches():
    session = db_session.create_session()
    today = datetime.datetime.today()
    old_searches = session.query(Search).filter(Search.start_date < today).all()
    for search in old_searches:
        search = deactivate_search(search)
    session.commit()
    session.close()

    return

def deactivate_search(search):
    search.is_active = False
    return search

def toggle_search_status(search_id, new_val):
    session = db_session.create_session()
    search = find_search_by_id(search_id)
    if not search:
        return False
    search.is_active = new_val
    session.add(search)
    session.commit()
    session.close()
    return True