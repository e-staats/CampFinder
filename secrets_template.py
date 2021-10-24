import os

def create_environment_variables():
    #fill these out prior to starting the app:
    os.environ["ADMIN_PASSWORD"] = ''
    os.environ["EMAIL_PASSWORD"] = ''
    os.environ["SECRET_KEY"] = ''
    os.environ["DISTANCE_MATRIX_API"] = ''
    os.environ["PLACE_API"] = ''
    os.environ["SENDGRID_API_KEY"] = ''
    return