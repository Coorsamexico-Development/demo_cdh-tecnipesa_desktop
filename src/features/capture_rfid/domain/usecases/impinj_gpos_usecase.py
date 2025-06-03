import enum
from features.shared.errors.request_error import RequestError
from PyQt6.QtCore import QThread, pyqtSignal
from features.capture_rfid.infrastructure.models.gpo_configuration_model import (
    GpoConfigurationModel)
from features.capture_rfid.infrastructure.datasource.api_impinj_gpos_datasource import (
    ApiImpinjGposDatasource)
from features.capture_rfid.infrastructure.constants.constants import COLORS_LED

class ImpinjGposUseCase:
    def __init__(self, datasource:ApiImpinjGposDatasource= ApiImpinjGposDatasource()):
        self.datasource = datasource

    def update_gpos(self, gpo_configurations:list[GpoConfigurationModel]) -> str:
        return self.datasource.update_gpos(gpo_configurations=gpo_configurations)
    
    


class ImpinjGposWoker(QThread):
    task_complete = pyqtSignal()

    
    def __init__(self):
        super().__init__()
        self.type = type
        self.gpos_cases = ImpinjGposUseCase()
        self.resp:str = ""
        self.color = 'off'
        self.has_error = False
        self.error = RequestError()

    def colorsLeds(self):
        num_color = COLORS_LED[self.color]
        bin_numers = list(bin(num_color)[2:].rjust(2, '0')[::-1])
        leds = [GpoConfigurationModel(
                gpo=index+1,
                state=GpoConfigurationModel.StateGeo.HIGH if bin_numer == '1' else GpoConfigurationModel.StateGeo.LOW
            )  for index,bin_numer  in enumerate(bin_numers)]
        
        return leds

    def run(self):
        try:
            self.resp = self.gpos_cases.update_gpos(gpo_configurations=self.colorsLeds())
        except RequestError as e:
            self.has_error = True
            self.error = e
        self.task_complete.emit()

# class ResponseGpos: 
#     def __init__(self):
#         self.resp:str = ""
#         self.has_error = False
#         self.error = RequestError()

    
