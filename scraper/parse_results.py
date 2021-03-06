import services.search_services as search_services
import services.user_services as user_services
import services.availability_services as avail_services
from services.email_services import ParkEmailer
import templates.email.availability_message as availability_message

# pylint: disable = no-member


def process_all_results():
    searches = search_services.find_active_searches()
    for search in searches:
        process_result(
            search.start_date, search.end_date, search.parks, search.owner_id
        )
    return


def process_result(start_date, end_date, parks, owner_id):
    # short circuit if the user doesn't want to be notified:
    user_prefs = user_services.get_user_preferences(owner_id)
    if user_prefs["email"] == False and user_prefs["text"] == False:
        return

    # check for results for the search and move on if there are no availabilities
    park_id_list = search_services.deserialize_park_list(parks)
    availability_info = avail_services.find_availability_info_for_date_range(
        start_date, end_date, park_id_list
    )
    if availability_info == []:
        return

    if user_prefs["email"] == True:
        # turn the results into an email
        message = convert_availability_to_message(
            availability_info, start_date, end_date
        )
        if message == False:
            return

        # grab the person to email:
        to_address = user_services.get_user_email(owner_id)
        if to_address == None:
            return

        # then send that email
        emailer = ParkEmailer()
        emailer.send_email(
            to_address=to_address,
            subject="New Campsite Availability for One of Your Searches!",
            html_message=message,
        )

    return


def convert_availability_to_message(availability_info, start_date, end_date):
    avail_dict = {}
    for a, p, r in availability_info:
        availability = str(a)
        try:
            avail_dict[availability].append((p, r))
        except:
            avail_dict[availability] = [(p, r)]

    if avail_dict == {}:
        return False
    message = availability_message.create_html(avail_dict, start_date, end_date)
    return message
