from sqlalchemy.sql.sqltypes import Boolean
from data.user import User  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
import services.email_services as email_service

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

def get_user_preferences(user_id):
    user = find_user_by_id(user_id)
    if user == None:
        return {}
    
    preferences = {}
    preferences["email"]=user.send_emails
    preferences["text"]=user.send_texts
    #expand as you add more preferences

    return preferences

def update_setting(user, setting_name, setting_status: Boolean):
    if user == None or setting_status == None:
        return False
    session = db_session.create_session()
    if setting_name == "email":
        user.send_emails = setting_status
    if setting_name == "text":
        user.send_texts = setting_status
    session.add(user)
    session.commit()
    session.close()

    return True


def create_user(name, email, password, security):

    # todo: validation
    if find_user_by_email(email):
        return None
    user = User()
    user.name = name
    user.email = email
    user.hashed_pw = hash_text(password)
    user.is_active = True
    user.security_class = security

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

def send_reset_email(email):
    user = find_user_by_email(email)
    if user==False:
        return False
    
    success = email_service.send_pw_reset_email(user.id, user.email)
    return success

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
    if len(password)<8:
        return "Password must be 8 characters or longer."
    if password.isalpha():
        return "Password must contain a number."
    if password.isnumeric():
        return "Password must contain a letter."
    return True

def validate_email(email):
    error_string = "Please check email format"
    if email.count("@") != 1:
        return error_string
    split_email = email.split("@")
    if len(split_email[0].strip())<1 or len(split_email[1].strip())<1:
        return error_string
    if split_email[1].count(".") == 0:
        return error_string
    domain_split = split_email[1].split(".")
    if len(domain_split[0])<1 or len(domain_split[1])<1:
        return error_string
    return True