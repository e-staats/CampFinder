from data.availability import Availability
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def create_message(reset_url):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Password reset for CampFinder"
    message["From"] = "wiparkscraper@gmail.com"

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(create_plaintext_body(reset_url),"plain",)
    part2 = MIMEText(create_html_body(reset_url),"html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    return message


# Create the plain-text and HTML version of your message
def create_plaintext_body(url):
    text = f"""\
            {greeting_text()} \n
            {url} \n
            {footer()}
            """
    return text


def create_html_body(url):
    html = f"""<html>
            <body>
                <p>
                {greeting_text()}<br>
                <a href="{url}">{url}</a>
                </p>
                <b><p>{footer()}</p></b>
            </body>
            </html>
            """
    return html


def greeting_text():
    return "Someone requested to reset the password for your CampFinder account. If you would like to reset your password, click here:"


def footer():
    return "If you didn't ask to reset your password, you should ignore this email."