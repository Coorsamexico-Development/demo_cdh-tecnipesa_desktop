
import json
from services.api_impinj_service import api_impinj
from features.shared.errors.request_error import RequestError
from  requests.exceptions import ConnectTimeout


class ApiImpinjDatasource:
    def __init__(self):
        pass

    def start_preset(self, preset_id:str)->str:
       

        try:
            response = api_impinj.post(f'/profiles/inventory/presets/{preset_id}/start')
            if not response.ok:
                error = json.loads(response.text)
                title = "Error al actualizar leds"
                if "message" in error:
                    message =error['message']
                else:
                    message = response.reason
                raise RequestError(title=title, message=message, code=response.status_code)

            return  "OK"
        
        except ConnectTimeout as e:
            raise RequestError(title="Sin conexion a la api",
                                message="LLevo mucho tiempo la solicitud al servidor asegurate de tener conexicón a Internet", 
                                code=500)
        except Exception as e:
            print(e)
            raise RequestError(title="Error",
                                message="Problemas con la API", 
                                code=500)
       

