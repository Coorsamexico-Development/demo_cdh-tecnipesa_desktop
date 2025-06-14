
import json
from services.api_impinj_service import api_impinj
from features.shared.errors.request_error import RequestError
from  requests.exceptions import ConnectTimeout
from features.capture_rfid.infrastructure.models.gpo_configuration_model import (
    GpoConfigurationModel)

class ApiImpinjGposDatasource:
    def __init__(self):
        pass

    def update_gpos(self, gpo_configurations:list[GpoConfigurationModel])->str:
        payload = json.dumps({
            "gpoConfigurations": [gpo_configuration.to_dict() for gpo_configuration in gpo_configurations]
        })   

        try:
            response = api_impinj.put('device/gpos', data=payload)
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
       

