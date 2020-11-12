from data.db_session import create_session # pylint: disable = import-error
from data.user import User  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
import datetime
from passlib.handlers.sha2_crypt import sha512_crypt as crypto


def find_user_by_id(user_id):
    session = db_session.create_session()

    user = session.query(User).filter(User.id == user_id).first()
    session.close()
    return user


def find_user_by_email(email):
    session = db_session.create_session()

    user = session.query(User).filter(User.email == email).first()
    session.close()
    return user


def get_user_email(user_id):
    session = db_session.create_session()

    user = session.query(User).filter(User.id == user_id).first()
    if user == None:
        return None
    session.close()
    return user.email


def create_user(name, email, password):

    # todo: validation
    if find_user_by_email(email):
        return None
    user = User()
    user.name = name
    user.email = email
    user.hashed_pw = hash_text(password)
    user.is_active = True

    session = db_session.create_session()
    session.expire_on_commit = False
    session.add(user)
    try:
        session.add(user)
        session.commit()
    finally:
        session.close()

    return user

def change_password(user_id, password):
    session = db_session.create_session()
    user = find_user_by_id(user_id)
    if user == None:
        return None
    user.hashed_pw = hash_text(password)    
    try:
        session.add(user)
        session.commit()
    finally:
        session.close()

    return user


def hash_text(text: str) -> str:
    hashed_text = crypto.encrypt(text, rounds=171204)
    return hashed_text


def verify_hash(hashed_text: str, plain_text: str) -> bool:
    return crypto.verify(plain_text, hashed_text)


def validate_user(email: str, password: str) -> User:
    user = find_user_by_email(email)
    if not user:
        return False
    if not verify_hash(user.hashed_pw, password):
        return False
    return user

def create_test_user(name, email, hashed_pw, active_status):
    u = User()
    u.name = name
    u.email = email
    u.hashed_pw = hashed_pw
    u.is_active = active_status
    return u

def validate_password(password):
    return True