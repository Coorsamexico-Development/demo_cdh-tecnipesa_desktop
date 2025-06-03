from PyQt6.QtCore import QThread, pyqtSignal
from features.shared.errors.request_error import RequestError
from features.home.datasource.api_impinj_datasource import ApiImpinjDatasource
import config.constants.enviroments as Enviroments



class ImpinjStartWoker(QThread):
    task_complete = pyqtSignal()

    
    def __init__(self):
        super().__init__()
        self.type = type
        self.api_impinj = ApiImpinjDatasource()

    def run(self):
        try:
            self.resp = self.api_impinj.start_preset(Enviroments.presetId)
        except RequestError as e:
            self.has_error = True
            self.error = e
        self.task_complete.emit()

