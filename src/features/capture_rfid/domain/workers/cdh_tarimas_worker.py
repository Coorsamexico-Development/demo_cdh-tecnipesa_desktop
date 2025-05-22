import enum
from PyQt6.QtCore import QThread, pyqtSignal

from features.shared.errors.request_error import RequestError
from features.capture_rfid.infrastructure.models.scaneo_model import ScaneoModel
from features.capture_rfid.infrastructure.datasource.api_loger_tarimas_datasource import (
    ApiLogerTarimasDatasource)
from typing import Union



class CdhTarimasWorker(QThread):
    task_complete = pyqtSignal(str)

    
    def __init__(self):
        super().__init__()
        self.scaneo:Union[ScaneoModel, None] = None
        self.api_cdh_tarimas = ApiLogerTarimasDatasource()
     
        self.has_error = False
        self.error = RequestError()

    def run(self):
        self.colorsResp = []
        try:
            color = self.api_cdh_tarimas.store_log(
                tarima_epc=self.scaneo.tag_inventory_event.epc,
                images=self.scaneo.images
                )
            self.scaneo.images.clear()
            self.task_complete.emit(color)
        except RequestError as e:
            self.has_error = True
            self.error = e
            self.task_complete.emit('yellow')

# class ResponseGpos: 
#     def __init__(self):
#         self.resp:str = ""
#         self.has_error = False
#         self.error = RequestError()

    
