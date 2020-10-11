import flask
import os
import sys
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
from scheduler import scheduler
from data.db_session import global_init


app = flask.Flask(__name__)
scheduler.init_app(app)
scheduler.start()


def main():
    register_blueprints()
    setup_db()
    app.run(debug=True)

def setup_db():
    db_file = os.path.join(os.path.dirname(__file__),'db','parkdb.sqlite')
    global_init(db_file)

def register_blueprints():
    from views import home_views

    app.register_blueprint(home_views.blueprint)


if __name__ == "__main__":
    main()