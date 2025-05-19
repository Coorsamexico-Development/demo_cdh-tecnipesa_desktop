
import config.constants.enviroments as Enviroments       
from services.request_service import RequestService

from requests.auth import HTTPBasicAuth

class ApiImpinjService(RequestService):
    def __init__(self,
               headers= {
                    'Accept': 'application/json',
                    'Content-Type': 'text/plain;charset=UTF-8',
              }
                 
                 ) -> None:
         super().__init__(
              baseUrl=Enviroments.apiIMPINJ,
              headers=headers
         )

api_impinj = ApiImpinjService()
basic_auth = HTTPBasicAuth(Enviroments.IMPINJ_USER, Enviroments.IMPINJ_PASSWORD)