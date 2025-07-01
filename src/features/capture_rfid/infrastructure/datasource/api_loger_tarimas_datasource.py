
import cv2
import json
from features.shared.errors.request_error import RequestError
from  requests.exceptions import ConnectTimeout
import io
import re
import numpy as np
from services.api_cdh_service import api_cdh_service
from features.capture_rfid.infrastructure.models.tag_inventory import TagInventory
from typing import Tuple
from features.capture_rfid.infrastructure.adapters.log_tarima_adapter import LogTarimaAdapter
from features.capture_rfid.infrastructure.models.log_tarima_model import LogTarimaModel

class ApiLogerTarimasDatasource:
    def __init__(self):
        pass

    def store_log(self, tag_inventory:TagInventory,images: np.ndarray)->str:
        payload = {
                    'token_tag': re.search(r'\b[0-9a-fA-F]+\b',tag_inventory.epc).group(),
                    'first_antenna': tag_inventory.first_antenna,
                    'second_antenna': tag_inventory.scond_antenna,
                }
        
        files= [('image[]',(f'image_{index}.jpg', imageToBytesIO(image), 'image/jpeg')) 
                for index,image in enumerate(images)]
        # files.pop()
        # files = []
      
        try:
            response = api_cdh_service.post('logtarima', data=payload, files=files)
            
            response = json.loads(response.content)
            if "data" in response:
                if "color" in response['data']:
                    color = response['data']['color']
                    # logTarima = LogTarimaAdapter.fromJson( response['data']['log_tarima'])
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
        

    def store_log_images(self, log_tarima_id:int, images: np.ndarray)->str:
        
        
        
        files= [('image[]',(f'image_{index}.jpg', imageToBytesIO(image), 'image/jpeg')) for index,image in enumerate(images)]

        try:
            response = api_cdh_service.post(f'logtarima/{log_tarima_id}/images', files=files)
            
            response = json.loads(response.content)
            if "data" in response:
                if "color" in response['data']:
                    color = response['data']['color']
                    return color
            if "color" in response:
                return response['color']
         
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
    
       

