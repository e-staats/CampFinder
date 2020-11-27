from data.security import Security
import data.db_session as db_session
import services.user_services as user_services
import os


def create_security_classes():
    session = db_session.create_session()
    session.add(create_default_user_class())
    session.add(create_admin_class())
    session.commit()
    return


def create_admin_class():
    security_class = Security()
    security_class.name = "admin"
    security_class.create_account = True
    return security_class


def create_default_user_class():
    security_class = Security()
    security_class.name = "default"
    security_class.create_account = False
    return security_class


def find_security_class_by_id(id):
    session = db_session.create_session()
    security = session.query(Security).filter(Security.id == id).first()
    session.close()
    return security


def find_admin_security_class():
    session = db_session.create_session()
    admin_class = session.query(Security).filter(Security.name == "admin").first()
    session.close()
    if admin_class == None:
        return None
    else:
        return admin_class.id


def find_default_security_class():
    session = db_session.create_session()
    default_class = session.query(Security).filter(Security.name == "default").first()
    session.close()
    if default_class == None:
        return None
    else:
        return default_class.id


def is_user_admin(user):
    session = db_session.create_session()
    admin_class = find_admin_security_class()
    if user.security_class == admin_class:
        return True
    else:
        return False


def classes_exist():
    session = db_session.create_session()
    classes = session.query(Security).first()
    if classes == None:
        session.close()
        return False
    session.close()
    return True


def create_admin_user():
    password = os.environ["ADMIN_PASSWORD"]
    security_class = find_admin_security_class()
    if security_class == None:
        raise Exception("Could not create admin: no security class found")
    user = user_services.create_user(
        "admin", "wiparkscraper@gmail.com", password, security_class
    )
    if not user:
        raise Exception("Could not create admin user.")
