# pylint thinks it can't find the infrastructure and viewmodels folders
# even though the app itself runs fine:
# pylint: disable = import-error

from viewmodels.shared.viewmodel_base import ViewModelBase
import services.user_services as user_service

class ActivateViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.user_id = self.request_dict.user_id

    def validate(self):
        if self.user_id == None:
            self.error = "An error occured. Please contact the site administrator."
        