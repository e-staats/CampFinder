import flask
import json
from werkzeug.datastructures import MultiDict


class RequestDictionary(dict):
    def __init__(self, *args, default_val=None, **kwargs):
        self.default_val = default_val
        super().__init__(*args, **kwargs)

    def __getattr__(self, key):
        return self.get(key, self.default_val)


def create(default_val=None, **route_args) -> RequestDictionary:
    request = flask.request

    # Adding this retro actively. Some folks are experiencing issues where they
    # are getting a list rather than plain dict. I think it's from multiple
    # entries in the multidict. This should fix it.
    args = request.args
    if isinstance(request.args, MultiDict):
        args = request.args.to_dict()

    form = request.form
    if isinstance(request.args, MultiDict):
        form = request.form.to_dict()

    data = {
        **args,  # The key/value pairs in the URL query string
        **request.headers,  # Header values
        **form,  # The key/value pairs in the body, from a HTML post form
        **route_args  # And additional arguments the method access, if they want them merged.
    }

    return RequestDictionary(data, default_val=default_val)

def data_create(default_val=None, **route_args) -> RequestDictionary:
    request = flask.request

    args = request.args
    if isinstance(request.args, MultiDict):
        args = request.args.to_dict()

    api_data = request.data
    if isinstance(request.args, MultiDict):
        api_data = json.loads(api_data)

    data = {
        **args,  # The key/value pairs in the URL query string
        **request.headers,  # Header values
        **api_data,  # The key/value pairs in the body, from a HTML post form
        **route_args  # And additional arguments the method access, if they want them merged.
    }

    return RequestDictionary(data, default_val=default_val)
