import enum
from PyQt6.QtCore import QThread, pyqtSignal

from features.shared.errors.request_error import RequestError
from features.capture_rfid.infrastructure.models.scaneo_model import ScaneoModel
from features.capture_rfid.infrastructure.datasource.api_loger_tarimas_datasource import (
    ApiLogerTarimasDatasource)
from typing import Union
from features.capture_rfid.infrastructure.models.log_tarima_model import LogTarimaModel




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

           
            images=self.scaneo.images.copy()
            color, log_tarima = self.api_cdh_tarimas.store_log(
                tag_inventory=self.scaneo.tag_inventory_event,
                )
            self.task_complete.emit(color)
            print(f"images: {len(images)}___________________")
            self.api_cdh_tarimas.store_log_images(
                log_tarima_id=log_tarima.id,
                images=images
                )
            self.log_tariam_id = None
            self.scaneo.images.clear()


                
                 

        except RequestError as e:
            self.has_error = True
            self.error = e
            self.task_complete.emit( 'yellow')



    
