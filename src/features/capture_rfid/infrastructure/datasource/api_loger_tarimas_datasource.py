
import cv2
import json
from features.shared.errors.request_error import RequestError
from  requests.exceptions import ConnectTimeout
import io

import numpy as np
from services.api_cdh_service import api_cdh_service

class ApiLogerTarimasDatasource:
    def __init__(self):
        pass

    def store_log(self, tarima_epc:str, image: np.ndarray)->str:
        payload = {'token_tag': tarima_epc}
        files= {'image': ('image.jpg', imageToBytesIO(image), 'image/jpeg')}

        try:
            response = api_cdh_service.post('logtarima', data=payload, files=files)
            # if not response.ok:
            #     error = json.loads(response.content)
            #     title = "Error al guardar el log de la tarima"
            #     if "message" in error:
            #         message =error['message']
            #     else:
            #         message = response.reason
            #     raise RequestError(title=title, message=message, code=response.status_code)
            
            response = json.loads(response.content)
            if "data" in response:
                if "color" in response['data']:
                    color = response['data']['color']
                    return color
                
         
            raise RequestError(title="Error al guardar el log de la tarima",
                                    message="No se ha podido guardar el log de la tarima", 
                                    code=response.status_code)
        
        except ConnectTimeout as e:
            raise RequestError(title="Sin conexion a la api",
                                message="LLevo mucho tiempo la solicitud al servidor asegurate de tener conexicón a Internet", 
                                code=500)
        except RequestError as e:
            raise e
        except Exception as e:
            print(e)
            raise RequestError(title="Error",
                                message="Problemas con la API", 
                                code=500)
        

def imageToBytesIO( image: np.ndarray) -> io.BytesIO:
    success, encoded_image = cv2.imencode('.jpg', image)
    if not success:
        raise ValueError("Could not encode image to JPEG format")
    return io.BytesIO(encoded_image.tobytes())
    
       

