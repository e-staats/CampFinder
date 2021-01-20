import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from services.url_services import set_up_url


def create_message(avail_dict, start_date, end_date):
    message = MIMEMultipart("alternative")
    message["Subject"] = "New Park Availability!"
    message["From"] = "wiparkscraper@gmail.com"

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(
        create_plaintext_body(
            create_park_list(avail_dict, start_date, end_date, html=False)
        ),
        "plain",
    )
    part2 = MIMEText(
        create_html_body(create_park_list(avail_dict, start_date, end_date, html=True)),
        "html",
    )

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    return message

# Create the plain-text and HTML version of your message
def create_plaintext_body(park_list):
    text = f"""\
            {greeting_text()} \n
            {park_list}
            {cancel_text_plaintext()} \n
            """
    return text


def create_html_body(park_list):
    html = f"""<html>
            <body>
                <p>
                {greeting_text()}<br>
                {park_list}
                </p>
                <b><p>{cancel_text_html()}</p></b>
            </body>
            </html>
            """
    return html


def create_park_list(avail_dict, start_date, end_date, string="", html=False, ):
    if html == True:
        linebreak = "<br>"
        emphasis_start = "<span style='color: green'>"
        emphasis_end = "</span>"
        header_start = "<b><u>"
        header_end = "</b></u>"
    else:
        linebreak = "\n"
        emphasis_start = "* "
        emphasis_end = ""
        header_start = "~"
        header_end = "~"

    for availability_range in avail_dict.keys():
        string = string + header_start + availability_range + header_end + linebreak
        for park, region in avail_dict[availability_range]:
            park_string = (
                emphasis_start
                + format_park(park, region.name, html, start_date, end_date)
                + emphasis_end
            )
            string = string + park_string + linebreak
    return string


def greeting_text():
    return "The following parks are available for your requested dates:"


def format_park(park, region, html, start_date, end_date):
    url = set_up_url(start_date, end_date, None, park.external_id)
    if html == False:
        return f"{park.name} - {region} ({url})"
    else:
        return f"""<a href="{url}">{park.name} - {region}</a>"""

def cancel_text_html():
    return "To stop receiving emails for this search, update your <a href='www.campfinder.me/account'>account page</a>."


def cancel_text_plaintext():
    return "To stop receiving emails for this search, update your account page: www.campfinder.me/account"

