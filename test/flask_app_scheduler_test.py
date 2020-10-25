import os
import sys
from global_test_setup import prep_db  # pylint: disable = import-error
import flask

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
from data.db_session import global_init  # pylint: disable = import-error
from scraper_shell import scrape_searches  # pylint: disable = import-error
import testing_tools


def register_blueprints(app):
    from views import home_views  # pylint: disable = import-error

    app.register_blueprint(home_views.blueprint)


if __name__ == "__main__":
    app = flask.Flask(__name__)
    register_blueprints(app)
    prep_db()
    testing_tools.setup_all_test_data()
    app.run(debug=False)