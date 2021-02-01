import itsdangerous as itsd
import os

from werkzeug.exceptions import ServiceUnavailable


def serialize_url_time_sensitive_value(value, salt):
    serializer = itsd.URLSafeTimedSerializer(os.environ["SECRET_KEY"])
    return serializer.dumps(value, salt)


def deserialize_url_time_sensitive_value(token, salt):
    serializer = itsd.URLSafeTimedSerializer(os.environ["SECRET_KEY"])
    try:
        decoded_payload = serializer.loads(token, salt=salt, max_age=86400)
        return decoded_payload
    except itsd.BadSignature as e:
        if e.payload is not None:
            try:
                decoded_payload = serializer.load_payload(e.payload)
                return None
            except itsd.BadData:
                return None

def serialize_value(value, salt):
    serializer = itsd.Serializer(os.environ["SECRET_KEY"])
    return serializer.dumps(value, salt)

def deserialize_value(token, salt):
    serializer = itsd.Serializer(os.environ["SECRET_KEY"])
    try:
        decoded_payload = serializer.loads(token, salt=salt)
        return decoded_payload
    except itsd.BadSignature as e:
        if e.payload is not None:
            try:
                decoded_payload = serializer.load_payload(e.payload)
                return None
            except itsd.BadData:
                return None

