from data.db_session import create_session
import services.search_services as search_services
import services.user_services as user_services
import services.availability_services as avail_services
from emailer import ParkEmailer
import email_message
from data.availability import Availability
from data.park import Park
from data.region import Region

# pylint: disable = no-member


def process_results():
    searches = search_services.find_active_searches()
    emailer = ParkEmailer()
    for search in searches:
        # check for results for the search and move on if there are no availabilities
        availability_info = avail_services.find_availability_info_for_date_range(
            search.start_date,
            search.end_date,
        )
        if availability_info == []:
            continue

        # turn the results into an email
        park_id_list = search_services.deserialize_park_list(search)
        message = convert_availability_to_message(availability_info, park_id_list)
        if message == False:
            continue

        # grab the person to email:
        to_address = user_services.get_user_email(
            search.owner_id,
        )
        if to_address == None:
            continue

        # then send that email
        message["To"] = to_address
        emailer.send_email(to_address, message)


def convert_availability_to_message(availability_info, park_id_list):
    avail_dict = {}
    for a, p, r in availability_info:
        availability = str(a)
        try:
            avail_dict[availability].append((p, r))
        except:
            avail_dict[availability] = [(p, r)]

    if avail_dict == {}:
        return False
    message = email_message.create_message(avail_dict, park_id_list)

    return message
