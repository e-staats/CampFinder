# pylint thinks it can't find the infrastructure and viewmodels folders
# even though the app itself runs fine:
# pylint: disable = import-error

import flask
import os
import sys

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)
from viewmodels.home.index_viewmodel import IndexViewModel
from infrastructure.view_modifiers import response
from flask import jsonify
from scraper_shell import setup_info_dict, start_scraper
from scheduler import scheduler

blueprint = flask.Blueprint("home", __name__, template_folder="templates")


@blueprint.route("/", methods=["GET"])
@response(template_file="home/index.html")
def index():
    vm = IndexViewModel()
    return vm.to_dict()


@blueprint.route("/", methods=["POST"])
@response(template_file="home/index.html")
def scraper_post():
    vm = IndexViewModel()
    #POC the scheduler:
    url_list = setup_info_dict()
    scheduler.add_job(id='manual-start-scraper', func=start_scraper, kwargs={"start_urls": url_list})
    return vm.to_dict()