# pylint thinks it can't find the infrastructure and viewmodels folders
# even though the app itself runs fine:
# pylint: disable = import-error

import sys
import os
from viewmodels.shared.viewmodel_base import ViewModelBase
import services.user_services as user_service

class LoginViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.email = self.request_dict.email.lower().strip()
        self.password = self.request_dict.password.strip()


    def validate(self):
        if not self.email or not self.email.strip():
            self.error = "You must specify an email"
        elif not self.password:
            self.error = "You must specify a password"
        self.user = user_service.validate_user(self.email,self.password)
        if not self.user:
            self.error = "The username or password is incorrect."