
import config.constants.enviroments as Enviroments       
from services.request_service import RequestService

class ApiCdhService(RequestService):
    def __init__(self,
               headers= {
                    'Accept': 'application/json',
              }
                 
                 ) -> None:
         super().__init__(
              baseUrl=Enviroments.apiUrl,
              headers=headers
         )

api_cdh_service = ApiCdhService()