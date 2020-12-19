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
        #short circuit if the user doesn't want to be notified:
        user_prefs = user_services.get_user_preferences(search.owner_id)
        if user_prefs['email']==False and user_prefs['text']==False:
            continue

        # check for results for the search and move on if there are no availabilities
        park_id_list = search_services.deserialize_park_list(search.parks)
        availability_info = avail_services.find_availability_info_for_date_range(
            search.start_date,
            search.end_date,
            park_id_list
        )
        if availability_info == []:
            continue

        if user_prefs['email'] == True:
            # turn the results into an email
            message = convert_availability_to_message(availability_info)
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


def convert_availability_to_message(availability_info):
    avail_dict = {}
    for a, p, r in availability_info:
        availability = str(a)
        try:
            avail_dict[availability].append((p, r))
        except:
            avail_dict[availability] = [(p, r)]

    if avail_dict == {}:
        return False
    message = email_message.create_message(avail_dict)

    return message
