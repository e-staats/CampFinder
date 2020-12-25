import hashlib
from datetime import timedelta
from typing import Optional

from flask import Request
from flask import Response

from infrastructure.num_convert import try_str # pylint: disable = import-error

auth_cookie_name = 'wi_park_scraper'


def set_auth(response: Response, user_id: int):
    hash_val = __hash_text(str(user_id))
    val = "{}:{}".format(user_id, hash_val)
    response.set_cookie(auth_cookie_name, val)


def __hash_text(text: str) -> str:
    text = 'salty__' + text + '__text'
    return hashlib.sha512(text.encode('utf-8')).hexdigest()


def __add_cookie_callback(_, response: Response, name: str, value: str):
    response.set_cookie(name, value, max_age=timedelta(days=30))


def get_user_id_via_auth_cookie(request: Request):
    if auth_cookie_name not in request.cookies:
        return None

    val = request.cookies[auth_cookie_name]
    parts = val.split(':')
    if len(parts) != 2:
        return None

    user_id = parts[0]
    hash_val = parts[1]
    hash_val_check = __hash_text(user_id)
    if hash_val != hash_val_check:
        print("Warning: Hash mismatch, invalid cookie value")
        return None

    return try_str(user_id)


def logout(response: Response):
    response.delete_cookie(auth_cookie_name)
