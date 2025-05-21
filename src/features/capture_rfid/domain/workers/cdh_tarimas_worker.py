import enum
from PyQt6.QtCore import QThread, pyqtSignal

from features.shared.errors.request_error import RequestError
from features.capture_rfid.infrastructure.models.scaneo_model import ScaneoModel
from features.capture_rfid.infrastructure.datasource.api_loger_tarimas_datasource import (
    ApiLogerTarimasDatasource)



class CdhTarimasWorker(QThread):
    task_complete = pyqtSignal()

    class Type(enum.Enum):
        Get = 1 # type: CdhTarimasWorker.Get
        Store = 2 # type: CdhTarimasWorker.Store
    
    def __init__(self, type: 'CdhTarimasWorker.Type' = Type.Get):
        super().__init__()
        self.type = type
        self.scaneos:list[ScaneoModel] = []
        self.api_cdh_tarimas = ApiLogerTarimasDatasource()
        self.colorsResp:list[str] = []
        self.has_error = False
        self.error = RequestError()

    def run(self):
        if self.type == CdhTarimasWorker.Type.Store:
            self.colorsResp = []
            for scaneo in self.scaneos:
                try:
                    color = self.api_cdh_tarimas.store_log(
                        tarima_epc=scaneo.tag_inventory_event.epc,
                        image=scaneo.image
                        )
                    self.colorsResp.append(color)
                    scaneo.image = None
                except RequestError as e:
                    self.has_error = True
                    self.error = e
        self.task_complete.emit()

# class ResponseGpos: 
#     def __init__(self):
#         self.resp:str = ""
#         self.has_error = False
#         self.error = RequestError()

    
