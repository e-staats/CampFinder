from data.security import Security
from services.user_services import find_user_by_id # pylint: disable = import-error
import services.security_services as security_services # pylint: disable = import-error
import flask
import infrastructure.cookie_auth as cookie # pylint: disable = import-error
import infrastructure.request_dict as request_dict # pylint: disable = import-error
from flask import Request

from typing import Optional

class ViewModelBase:
    def __init__(self):
        self.request: Request = flask.request
        self.request_dict = request_dict.create('')

        self.error: Optional[str] = None
        self.user_id = cookie.get_user_id_via_auth_cookie(self.request)
        if self.user_id:
            self.user = find_user_by_id(self.user_id)
            self.user_name = self.user.name
            self.admin = security_services.is_user_admin(self.user) 

    def to_dict(self):
        return self.__dict__
