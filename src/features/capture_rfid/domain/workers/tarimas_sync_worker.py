from PyQt6.QtCore import QThread, pyqtSignal

from features.shared.errors.request_error import RequestError
from features.capture_rfid.infrastructure.datasource.api_tarimas_datasource import (
    ApiTarimasDatasource)
from features.capture_rfid.infrastructure.datasource.db_tarimas_datasource import (
    DBTarimasDatasource)
from features.database.models.tarima import Tarima
from features.shared.errors.sql_error import SqlError
from typing import Union
from features.database.managers.sqlite_manager import SqlliteManager




class TarimasSyncWorker(QThread):
    task_complete = pyqtSignal(bool)
   
    
    def __init__(self):
        super().__init__()
        self.api_tarimas = ApiTarimasDatasource()
        self.db_tarimas = DBTarimasDatasource()
     
        self.has_error = False
        self.error:Union[SqlError,RequestError] = SqlError()

    def run(self):
        sqlite_manager = SqlliteManager()
        try:
            last_tarima = Tarima.select('*').orderBy('tarimas.updated_at', 'desc').first()
            next_page = None
            updated_at = last_tarima.updated_at.replace("/", "-") if last_tarima else None
            print(updated_at)
            while True:
                tarimas_paginated = self.api_tarimas.get_pagination(
                    updated_at=updated_at,
                    next_page_url= next_page,
                )
                for tarima in tarimas_paginated.data:
                    self.db_tarimas.updateOrCreate(tarima)
                print(f"next_page: {tarimas_paginated.next_page_url}")
                next_page = tarimas_paginated.next_page_url
                
                if next_page is None:
                    break

                
            self.task_complete.emit(True)      

        except RequestError as e:
            self.has_error = True
            self.error = e
            self.task_complete.emit(False)
        except SqlError as e:
            self.has_error = True
            self.error = e
            self.task_complete.emit(False)
        finally:
            sqlite_manager.close_connection()
            



    
