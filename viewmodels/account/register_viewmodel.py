# pylint thinks it can't find the infrastructure and viewmodels folders
# even though the app itself runs fine:
# pylint: disable = import-error

import sys
import os
from viewmodels.shared.viewmodel_base import ViewModelBase
import services.user_services as user_service

class RegisterViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.name = self.request_dict.name
        self.email = self.request_dict.email.lower().strip()
        self.password = self.request_dict.password.strip()


    def validate(self):
        if not self.email or not self.email.strip():
            self.error = "You must specify an email"
        elif user_service.find_user_by_email(self.email):
            self.error = 'A user with that email address already exists.'
        elif not self.name or not self.name.strip():
            self.error = "You must specify a name"
        elif not self.password:
            self.error = "You must specify a password"
        elif len(self.password.strip()) < 1:
            self.error = 'The password must be at least 1 characters.'

