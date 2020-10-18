from data.user import User  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
import datetime


def create_user(name, email, hashed_pw, active_status):
    u = User()
    u.name = name
    u.email = email
    u.hashed_pw = hashed_pw
    u.is_active = active_status
    return u


def find_user_by_id(user_id, session=None):
    if session == None:
        session = db_session.create_session()

    user = (
        session.query(User)
        .filter(User.id == user_id)
        .first()
    )

    return user