import flask
import os
import sys
import datetime

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
from data.db_session import global_init
from scraper_shell import scrape_searches

def setup_db():
    db_file = os.path.join(os.path.dirname(__file__), "db", "parkdb.sqlite")
    global_init(db_file)


def register_blueprints(app):
    from views import home_views
    from views import account_views

    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(account_views.blueprint)


if __name__ == "__main__":
    app = flask.Flask(__name__)
    register_blueprints(app)
    setup_db()
    app.run(debug=True)