# pylint thinks it can't find the infrastructure and viewmodels folders
# even though the app itself runs fine:
# pylint: disable = import-error

from viewmodels.shared.viewmodel_base import ViewModelBase
import services.user_services as user_service

class ChangePwViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.old_password = self.request_dict.old_password.strip()
        self.new_password = self.request_dict.new_password.strip()
        self.confirm_password = self.request_dict.confirm_password.strip()


    def validate(self):
        if not self.old_password:
            self.error = "You must enter your old password"
        elif not self.new_password:
            self.error = "You must enter a new password"
        elif not self.confirm_password:
            self.error = "You must re-enter your new password"
        if self.new_password != self.confirm_password:
            self.error = "You new passwords must match"
        self.user = user_service.validate_user(self.user.email,self.old_password)
        if not self.user:
            print(self.user)
            print(self.old_password)
            print(self.new_password)
            print(self.confirm_password)
            print(self.user)
            self.error = "The old password is incorrect."
        password_validation = user_service.validate_password(self.old_password)
        if password_validation != True:
            self.error = password_validation
        