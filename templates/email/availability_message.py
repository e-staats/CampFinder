from services.url_services import set_up_url


def create_html(avail_dict, start_date, end_date):
    html_message = create_html_body(
        create_park_list(avail_dict, start_date, end_date)
    )
    return html_message


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


def create_park_list(avail_dict, start_date, end_date, string=""):
    linebreak = "<br>"
    emphasis_start = "<span style='color: green'>"
    emphasis_end = "</span>"
    header_start = "<b><u>"
    header_end = "</b></u>"
    for availability_range in avail_dict.keys():
        string = string + header_start + availability_range + header_end + linebreak
        for park, region in avail_dict[availability_range]:
            park_string = (
                emphasis_start
                + format_park(park, region.name, start_date, end_date)
                + emphasis_end
            )
            string = string + park_string + linebreak
    return string


def greeting_text():
    return "The following parks are available for your requested dates:"


def format_park(park, region, start_date, end_date):
    url = set_up_url(start_date, end_date, None, park.external_id)
    return f"""<a href="{url}">{park.name} - {region}</a>"""


def cancel_text_html():
    return "To stop receiving emails for this search, update your <a href='www.campfinder.me/account'>account page</a>."