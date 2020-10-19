"""
for each user who has an active search:
    for each active search
    check the results to see what parks are available
    create a dictionary of available parks and their region
    smush that into an email message
    find all users interested in a search
    email those users with the message
"""

from logging import info
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
        availability_info = avail_services.find_availability_info_for_date_range(
            search.start_date, search.end_date, session=session
        )
        if availability_info == None:
            continue
        message = convert_availability_to_message(availability_info)
        if message == False:
            return
        # users = search_services.find_users_interested_in_search(
        #     search.id, session=session
        # )
        # email_list = []
        # for user in users:
        #     email_list.append(user_services.get_user_email(user.id, session=session))
        # emailer = ParkEmailer()
        # success = emailer.email_users(email_list, message)
        # if success != True:
        #     pass  # todo
        print(message)
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
