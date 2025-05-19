import enum
from features.shared.errors.request_error import RequestError
from PyQt6.QtCore import QThread, pyqtSignal
from features.capture_rfid.infrastructure.models.gpo_configuration_model import (
    GpoConfigurationModel)
from features.capture_rfid.infrastructure.datasource.api_impinj_gpos_datasource import (
    ApiImpinjDatasource)

class ImpinjGposUseCase:
    def __init__(self, datasource:ApiImpinjDatasource= ApiImpinjDatasource()):
        self.datasource = datasource

    def update_gpos(self, gpo_configurations:list[GpoConfigurationModel]) -> str:
        return self.datasource.update_gpos(gpo_configurations=gpo_configurations)
    
    


class ImpinjGposWoker(QThread):
    task_complete = pyqtSignal()

    class Type(enum.Enum):
        Update = 1 # type: ImpinjGposWoker.Update
        Get = 2 # type: ImpinjGposWoker.Get
    
    def __init__(self, type: 'ImpinjGposWoker.Type' = Type.Get, **parmas):
        super().__init__()
        self.type = type
        self.params = parmas
        self.gpos_cases = ImpinjGposUseCase()
        self.resp:str = ""
        self.has_error = False
        self.error = RequestError()

    def run(self):
        try:
            if self.type == ImpinjGposWoker.Type.Update:
                self.resp = self.gpos_cases.update_gpos(**self.params)
        except RequestError as e:
            self.has_error = True
            self.error = e
        self.task_complete.emit()

# class ResponseGpos: 
#     def __init__(self):
#         self.resp:str = ""
#         self.has_error = False
#         self.error = RequestError()

    
