# pylint thinks it can't find the infrastructure and viewmodels folders
# even though the app itself runs fine:
# pylint: disable = import-error

import sys
import os
from viewmodels.shared.viewmodel_base import ViewModelBase
import services.user_services as user_service

class ForgotPwViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.email = self.request_dict.email.lower().strip()


    def validate(self):
        if not self.email or not self.email.strip():
            self.error = "You must specify an email"
        email_validation = user_service.validate_email(self.email)
        if email_validation != True:
            self.error = email_validation