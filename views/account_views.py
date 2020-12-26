# pylint thinks it can't find the infrastructure and viewmodels folders
# even though the app itself runs fine:
# pylint: disable = import-error
from flask import json
import services.search_services as search_services
import flask
from infrastructure.view_modifiers import response
import infrastructure.cookie_auth as cookie
import services.user_services as user_service
import services.security_services as security_service
import services.token_services as token_service
from viewmodels.account.index_viewmodel import IndexViewModel
from viewmodels.account.register_viewmodel import RegisterViewModel
from viewmodels.account.login_viewmodel import LoginViewModel
from viewmodels.account.change_pw_viewmodel import ChangePwViewModel
from viewmodels.account.forgot_pw_viewmodel import ForgotPwViewModel
from viewmodels.account.reset_pw_viewmodel import ResetPwViewModel
from viewmodels.account.activate_viewmodel import ActivateViewModel
import infrastructure.request_dict as request_dict
from data.user import User
from flask import jsonify, request
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
    if hasattr(vm, "user") == False:
        return {"admin": False}
    if vm.user_id and vm.admin:
        return {"admin": True}
    elif vm.user_id:
        return flask.redirect("/account")
    return {"admin": False}


@blueprint.route("/account/register", methods=["POST"])
@response(template_file="account/register.html")
def register_post():
    vm = RegisterViewModel()
    vm.validate()

    # for the beta:
    if vm.admin != True:
        vm.error = "Account creation is limited during the closed beta."

    if vm.error:
        return vm.to_dict()

    security_class = security_service.find_default_security_class()
    user = user_service.create_user(vm.name, vm.email, vm.password, security_class)
    if not user:
        vm.error = "The account could not be created"
        return vm.to_dict()
    
    success = user_service.send_activation_email(user)
    if success != True:
        vm.error = "The activation email failed to send. Please contact the site administrator for help."
        return vm.to_dict()
    
    resp = flask.redirect("/")

    return resp


# ################### ACTIVATE ACCOUNT #################################


@blueprint.route("/account/activate_account", methods=["GET", "POST"])
@response(template_file="account/activate.html")
def activate_account():
    vm = ActivateViewModel()
    token = request.args.get("token")
    if token == None:
        return flask.redirect("/")
    user_id = token_service.deserialize_url_time_sensitive_value(token, "activate")
    user = user_service.find_user_by_id(user_id)
    if user_id == None or user == None:
        return flask.redirect("/")
    vm.user_id = user_id
    success = user_service.activate_user(user)
    if success != True:
        vm.error = "We ran into an issue activating your account. Please contact the site admin for help."
        return vm.to_dict()
    resp = flask.redirect("/account/confirmation")
    return resp

@blueprint.route("/account/confirmation", methods=["GET", "POST"])
@response(template_file="account/confirmation.html")
def confirmation():
    vm = IndexViewModel()
    
    return vm.to_dict()


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


# ################### FORGOT PASSWORD #################################


@blueprint.route("/account/forgot_password", methods=["GET"])
@response(template_file="account/forgot_password.html")
def forgot_pw_get():
    vm = ForgotPwViewModel()
    return vm.to_dict()


@blueprint.route("/account/forgot_password", methods=["POST"])
@response(template_file="account/forgot_password.html")
def forgot_pw_post():
    vm = ForgotPwViewModel()
    vm.validate()
    if vm.error:
        return vm.to_dict()

    success = user_service.send_reset_email(vm.email)
    if not success:
        vm.error = "We could not send an email to this address. Please contact the site administrator for help."
        return vm.to_dict()

    vm.success = "A pasword reset email was sent to that address."

    return vm.to_dict()


# ################### RESET PASSWORD #################################


@blueprint.route("/account/reset_password", methods=["GET"])
@response(template_file="account/reset_password.html")
def reset_pw_get():
    vm = ResetPwViewModel()
    token = request.args.get("token")
    if token == None:
        return flask.redirect("/")
    user_id = token_service.deserialize_url_time_sensitive_value(
        token, "reset_password"
    )
    if user_id == None or user_service.find_user_by_id(user_id) == None:
        return flask.redirect("/")
    vm.user_id = token_service.serialize_value(user_id, "reset_user")
    return vm.to_dict()


@blueprint.route("/account/reset_password", methods=["POST"])
@response(template_file="account/reset_password.html")
def reset_pw_post():
    vm = ResetPwViewModel()
    vm.validate()
    if vm.error:
        return vm.to_dict()

    user_id = token_service.deserialize_value(vm.user_id, "reset_user")
    if user_id == None or user_service.find_user_by_id(user_id) == None:
        vm.error = "Failed to reset password for this user."

    user = user_service.change_password(user_id, vm.new_password)
    if not user:
        vm.error = "We could not change the password for this user. Please contact the site administrator for help."
        return vm.to_dict()

    vm.success = "Password successfully changed."

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
    success = search_services.toggle_search_status(request["id"], request["is_active"])
    if not success:
        return jsonify({"status": "could not find search"})

    return jsonify({"status": "success"})


# #################### SETTINGS FUNCTIONS ######################


@blueprint.route("/account/_load_user_preferences", methods=["GET"])
@response(template_file="account/settings.html")
def load_user_preferences():
    vm = IndexViewModel()
    if not vm.user_id:
        return flask.redirect("account/login")

    preferences = user_service.get_user_preferences(vm.user_id)
    if preferences == {}:
        return jsonify("status: no preferences")

    return jsonify(preferences)


@blueprint.route("/account/_toggle_setting_status", methods=["POST"])
@response(template_file="account/settings.html")
def toggle_setting_status():
    vm = IndexViewModel()
    if not vm.user_id:
        return flask.redirect("account/login")

    request = request_dict.data_create("")

    success = user_service.update_setting(
        vm.user, request["setting"], request["is_checked"]
    )
    if not success:
        return jsonify({"status": "could not update setting"})

    return jsonify({"status": "success"})