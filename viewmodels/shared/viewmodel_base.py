import flask
from flask import Request
import bson

from typing import Optional

class ViewModelBase:
    def __init__(self):
        self.request: Request = flask.request

    def to_dict(self):
        return self.__dict__
