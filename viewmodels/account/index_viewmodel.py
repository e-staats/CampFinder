# pylint thinks it can't find the infrastructure and viewmodels folders
# even though the app itself runs fine:
# pylint: disable = import-error

from viewmodels.shared.viewmodel_base import ViewModelBase

class IndexViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.search_list = []


