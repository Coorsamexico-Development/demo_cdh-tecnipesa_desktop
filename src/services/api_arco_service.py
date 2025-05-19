
import config.constants.enviroments as Enviroments       
from services.request_service import RequestService

class ApiArcoService(RequestService):
    def __init__(self,
               headers= {
                    'Accept': 'application/json',
              }
                 
                 ) -> None:
         super().__init__(
              baseUrl=Enviroments.apiArco,
              headers=headers
         )

api_mark = ApiArcoService()