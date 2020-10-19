from data.availability import Availability
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create the plain-text and HTML version of your message
def create_plaintext_body(park_list):
    text = f"""\
            {greeting_text()} \n
            {park_list}
            {cancel_text} \n
            """
    return text


def create_html_body(park_list):
    html = f"""<html>
            <body>
                <p>{greeting_text()}<br>
                {park_list}
                <b><p>{cancel_text()}</p></b>
                </p>
            </body>
            </html>
            """
    return html


def create_park_list(avail_dict, string="", html=False):
    if html == True:
        linebreak = "<br>"
    else:
        linebreak = "\n"
    for a in avail_dict.keys():
        string = string + str(a) + linebreak
        for p, r in avail_dict[a]:
            string = string + p.name + " - " + r.name + linebreak
    return string


def greeting_text():
    return "The following parks are available for your requested dates:"

def cancel_text():
    return "To stop receiving emails for this search, click here (todo)"

def create_message(avail_dict):
    message = MIMEMultipart("alternative")
    message["Subject"] = "New Park Availability!"
    message["From"] = "wiparkscraper@gmail.com"

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(
        create_plaintext_body(create_park_list(avail_dict, html=False)), "plain"
    )
    part2 = MIMEText(create_html_body(create_park_list(avail_dict, html=True)), "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    return message


# Create secure connection with server and send email
def send_that_email(message):
    sender_email = "wiparkscraper@gmail.com"
    receiver_email = "eric.k.staats@gmail.com"
    context = ssl.create_default_context()
    password = "sickpassword"
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
