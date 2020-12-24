# pylint thinks it can't find the infrastructure and viewmodels folders
# even though the app itself runs fine:
# pylint: disable = import-error

from viewmodels.shared.viewmodel_base import ViewModelBase
import services.user_services as user_service

class ResetPwViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.new_password = self.request_dict.new_password.strip()
        self.confirm_password = self.request_dict.confirm_password.strip()
        self.user_id = self.request_dict.user_id

    def validate(self):
        if self.user_id == None:
            self.error = "An error occured. Please contact the site administrator."
        if not self.new_password:
            self.error = "You must enter a new password"
        elif not self.confirm_password:
            self.error = "You must re-enter your new password"
        if self.new_password != self.confirm_password:
            self.error = "You new passwords must match"
        password_validation = user_service.validate_password(self.new_password)
        if password_validation != True:
            self.error = password_validation
        