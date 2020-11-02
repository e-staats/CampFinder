# pylint thinks it can't find the infrastructure and viewmodels folders
# even though the app itself runs fine:
# pylint: disable = import-error
import flask
from infrastructure.view_modifiers import response
import infrastructure.cookie_auth as cookie
import services.user_services as user_service
from viewmodels.account.index_viewmodel import IndexViewModel
from viewmodels.account.register_viewmodel import RegisterViewModel
from viewmodels.account.login_viewmodel import LoginViewModel
from data.user import User
# pylint: disable=no-member

blueprint = flask.Blueprint('account', __name__, template_folder='templates')

# ################### INDEX #################################

@blueprint.route('/account')
@response(template_file='account/settings.html')
def index():
    vm = IndexViewModel()
    if not vm.user_id:
        return flask.redirect('account/login')

    return vm.to_dict()

# ################### REGISTER #################################

@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    vm = RegisterViewModel()
    if vm.user_id:
        return flask.redirect('/account')
    return {}


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    vm = RegisterViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()
    
    user = user_service.create_user(vm.name, vm.email, vm.password)
    if not user:
        vm.error = "The account could not be created"
        return vm.to_dict()
    
    resp = flask.redirect('/')
    cookie.set_auth(resp, user.id)

    return resp


# ################### LOGIN #################################

@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    vm = LoginViewModel()
    if vm.user_id:
        return flask.redirect('/account')
    return vm.to_dict()


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    vm =LoginViewModel()
    vm.validate()

    if vm.error:
        return vm.to_dict()
    
    #todo: log in browser as session
    resp = flask.redirect('/')
    cookie.set_auth(resp, str(vm.user.id))

    return resp


# ################### LOGOUT #################################

@blueprint.route('/account/logout')
def logout():
    resp = flask.redirect("/")
    cookie.logout(resp)
    return resp