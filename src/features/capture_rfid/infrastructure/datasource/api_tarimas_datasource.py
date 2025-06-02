
import json
from features.shared.errors.request_error import RequestError

from  requests.exceptions import ConnectTimeout

from services.api_cdh_service import api_cdh_service
from features.capture_rfid.infrastructure.adapters.tarima_pagination_adapter import (
    TarimaPaginationAdapter)
from typing import Union
from features.capture_rfid.infrastructure.models.tarima_pagination_model import (
    TarimaPaginationModel)


class ApiTarimasDatasource:
    def __init__(self):
        pass

    def get_pagination(self,page:int = 1, 
                       per_page:int= 100, 
                       updated_at:Union[str, None]= None,
                       next_page_url:Union[str, None]= None,
                       )->TarimaPaginationModel:

        params = {}
        
        if not next_page_url:
            params['page'] = page

            if updated_at:
                params['updated_at'] = updated_at
            if per_page:
                params['per_page'] = per_page

        try:
            response = api_cdh_service.get(
               next_page_url if next_page_url else "tarima", params=params)
            if not response.ok:
                error = json.loads(response.text)
                title = "Error al obtener las Tarimas"
                if "message" in error:
                    message =error['message']
                else:
                    message = response.reason
                raise RequestError(title=title, message=message, code=response.status_code)
            jsonResponse = response.json()
           

            return TarimaPaginationAdapter.fromJson(jsonResponse)
        except ConnectTimeout as e:
            raise RequestError(title="Sin conexion a la api",
                                message="LLevo mucho tiempo la solicitud al servidor asegurate de tener conexicón a Internet", 
                                code=500)
        except RequestError as e:
            raise RequestError(title=e.title,
                                message=e.message, 
                                code=500)
        except Exception as e:
            print(e)
            raise RequestError(title="Error",
                                message="Problemas con la API al obtener las tarimas", 
                                code=500)
        
    



    