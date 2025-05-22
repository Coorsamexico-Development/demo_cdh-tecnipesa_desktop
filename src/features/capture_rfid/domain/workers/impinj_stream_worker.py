from PyQt6.QtCore import QThread, pyqtSignal
from requests.exceptions import ConnectTimeout
from services.api_impinj_service import api_impinj
from features.shared.errors.request_error import RequestError



class ImpinjStreamWorker(QThread):
    new_data = pyqtSignal()
    error = pyqtSignal()

    

    def run(self):
        try:
            with api_impinj.get('/data/stream', stream=True) as response:
               

                for line in response.iter_lines():
                    if line:
                        self.new_data.emit(line.decode('utf-8'))
        
        except ConnectTimeout as e:
            self.error.emit(RequestError(title="Sin conexion a la api",
                                message="LLevo mucho tiempo la solicitud al servidor asegurate de tener conexicón a Internet", 
                                code=500))
        except RequestError as e:
            self.error.emit(e)
        except Exception as e:
            self.error.emit(RequestError(title="Error",
                                message="Problemas con la API", 
                                code=500))

