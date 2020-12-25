from data.availability import Availability
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class BasicEmail:
    def __init__(self, subject, div1, div2, div3):
        self.subject = subject
        self.div1 = div1
        self.div2 = div2
        self.div3 = div3

    def create_message(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = "wiparkscraper@gmail.com"

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(
            self.create_plaintext_body(),
            "plain",
        )
        part2 = MIMEText(self.create_html_body(), "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        return message

    # Create the plain-text and HTML version of your message
    def create_plaintext_body(self):
        text = f"""\
                {self.div1} \n
                {self.div2} \n
                {self.div3}
                """
        return text

    def create_html_body(self):
        html = f"""<html>
                <body>
                    <div>
                        {self.div1}
                    </div>
                    <div>
                        {self.div2}
                    </div>
                    <div>
                        {self.div3}
                    </div>
                </body>
                </html>
                """
        return html