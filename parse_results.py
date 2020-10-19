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
    session = create_session()
    searches = search_services.find_active_searches(session=session)
    for search in searches:
        # check for results for the search and move on if there are no availabilities
        availability_info = avail_services.find_availability_info_for_date_range(
            search.start_date, search.end_date, session=session
        )
        if availability_info == []:
            continue

        # turn the results into an email
        message = convert_availability_to_message(availability_info)
        if message == False:
            continue

        # grab the person to email:
        to_address = user_services.get_user_email(search.owner_id, session=session)
        if to_address == None:
            continue

        # then send that email!
        emailer = (
            ParkEmailer()
        )  # todo: get the emailer class working. Right now if just hangs for 10 minutes and does nothing unless you ctrl+C out
        message["To"] = to_address
        email_message.send_that_email(message)


def convert_availability_to_message(availability_info):
    avail_dict = {}
    for a, p, r in availability_info:
        try:
            avail_dict[a] = avail_dict[a].append((p, r))
        except:
            avail_dict[a] = [(p, r)]

    if avail_dict == {}:
        return False
    message = email_message.create_message(avail_dict)

    return message
