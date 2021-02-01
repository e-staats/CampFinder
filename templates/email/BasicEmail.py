class BasicEmailBody:
    def __init__(self, div1, div2, div3):
        self.div1 = div1
        self.div2 = div2
        self.div3 = div3

    def create_message(self):
        html = self.create_html_body()
        return html

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