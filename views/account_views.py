# pylint thinks it can't find the infrastructure and viewmodels folders
# even though the app itself runs fine:
# pylint: disable = import-error
from flask import json
import services.search_services as search_services
import flask
from infrastructure.view_modifiers import response
import infrastructure.cookie_auth as cookie
import services.user_services as user_service
from viewmodels.account.index_viewmodel import IndexViewModel
from viewmodels.account.register_viewmodel import RegisterViewModel
from viewmodels.account.login_viewmodel import LoginViewModel
from viewmodels.account.change_pw_viewmodel import ChangePwViewModel
import infrastructure.request_dict as request_dict
from data.user import User
from flask import jsonify
import pprint

# pylint: disable=no-member

blueprint = flask.Blueprint("account", __name__, template_folder="templates")

# ################### INDEX #################################


@blueprint.route("/account")
@response(template_file="account/settings.html")
def index():
    vm = IndexViewModel()
    if not vm.user_id:
        return flask.redirect("account/login")

    searches = search_services.find_all_searches_for_user(vm.user_id)
    if searches == []:
        return vm.to_dict()

    for search in searches:
        vm.search_list.append(search_services.convert_to_dict(search))

    return vm.to_dict()


# ################### REGISTER #################################


@blueprint.route("/account/register", methods=["GET"])
@response(template_file="account/register.html")
def register_get():
    vm = RegisterViewModel()
    if vm.user_id:
        return flask.redirect("/account")
    return {}


@blueprint.route("/account/register", methods=["POST"])
@response(template_file="account/register.html")
def register_post():
    vm = RegisterViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    user = user_service.create_user(vm.name, vm.email, vm.password)
    if not user:
        vm.error = "The account could not be created"
        return vm.to_dict()

    resp = flask.redirect("/")
    cookie.set_auth(resp, user.id)

    return resp


# ################### LOGIN #################################


@blueprint.route("/account/login", methods=["GET"])
@response(template_file="account/login.html")
def login_get():
    vm = LoginViewModel()
    if vm.user_id:
        return flask.redirect("/account")
    return vm.to_dict()


@blueprint.route("/account/login", methods=["POST"])
@response(template_file="account/login.html")
def login_post():
    vm = LoginViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    # todo: log in browser as session
    resp = flask.redirect("/")
    cookie.set_auth(resp, str(vm.user.id))

    return resp


# ################### CHANGE PASSWORD #################################


@blueprint.route("/account/change_password", methods=["GET"])
@response(template_file="account/change_password.html")
def change_pw_get():
    vm = ChangePwViewModel()
    if not vm.user_id:
        return flask.redirect("/")
    return vm.to_dict()


@blueprint.route("/account/change_password", methods=["POST"])
@response(template_file="account/change_password.html")
def change_pw_post():
    vm = ChangePwViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    user = user_service.change_password(vm.user_id, vm.new_password)
    if not user:
        vm.error = "The password could not be changed. Please contact the site administrator for help."
        return vm.to_dict()

    vm.success = "Your password was successfully changed"
    vm.new_password = ""
    vm.old_password = ""
    vm.confirm_password = ""

    return vm.to_dict()


# ################### LOGOUT #################################


@blueprint.route("/account/logout")
def logout():
    resp = flask.redirect("/")
    cookie.logout(resp)
    return resp


# #################### SEARCH FUNCTIONS ######################


@blueprint.route("/account/_load_search_list", methods=["GET"])
@response(template_file="account/settings.html")
def load_search_list():
    vm = IndexViewModel()
    if not vm.user_id:
        return flask.redirect("account/login")

    searches = search_services.find_all_searches_for_user(vm.user_id)
    if searches == []:
        return jsonify({"searchList": None})

    search_list = []
    for search in searches:
        search_list.append(search_services.convert_to_dict(search))

    return jsonify({"searchList": search_list})


@blueprint.route("/account/_toggle_search_status", methods=["POST"])
@response(template_file="account/settings.html")
def toggle_search_status():
    vm = IndexViewModel()
    if not vm.user_id:
        return flask.redirect("account/login")

    request = request_dict.data_create("")
    pprint.pprint(request)

    success = search_services.toggle_search_status(request["id"], request["is_active"])
    if not success:
        return jsonify({"status": "could not find search"})

    return jsonify({"status": "success"})