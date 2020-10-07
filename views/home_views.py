import flask
import os
import sys
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)
from viewmodels.home.index_viewmodel import IndexViewModel
from infrastructure.view_modifiers import response
from flask import jsonify
from scraper_shell import setup_url_list,start_scraper,doodle

blueprint = flask.Blueprint('home', __name__, template_folder='templates')

@blueprint.route('/', methods=['GET'])
@response(template_file="home/index.html")
def index():
    vm = IndexViewModel()
    return vm.to_dict()

@blueprint.route('/', methods=['POST'])
@response(template_file="home/index.html")
def scraper_post():
    vm = IndexViewModel()
    url_list=setup_url_list()
    start_scraper(url_list)
    return vm.to_dict()