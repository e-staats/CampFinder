import flask
import os
import sys
import datetime
import secrets

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
from data.db_session import global_init
from scraper_shell import scrape_searches
import services.region_services as region_services
import services.park_services as park_services
import services.security_services as security_services

def setup_db():
    db_file = os.path.join(os.path.dirname(__file__), "db", "parkdb.sqlite")
    global_init(db_file)
    if not region_services.regions_exist():
        region_services.populate_regions()
    if not park_services.parks_exist():
        park_services.populate_parks()
    if not security_services.classes_exist():
        security_services.create_security_classes()
        print("created security classes")
        security_services.create_admin_user()
        print("Created admin user")


def register_blueprints(app):
    from views import home_views
    from views import account_views

    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(account_views.blueprint)


if __name__ == "__main__":
    app = flask.Flask(__name__)
    register_blueprints(app)
    secrets.create_environment_variables()
    setup_db()
    app.run(debug=True)