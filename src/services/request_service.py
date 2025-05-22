import requests
from typing import Union,Tuple


class RequestService():
    def __init__(self, baseUrl = '', headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                auth: Union[Tuple[str,str], None]= None, 
    ):
        super().__init__()
        self.baseUrl = baseUrl
        self.headers = headers
        if auth:
            self.request = requests.Session()
            self.request.auth = auth
        else:
            self.request = requests




    def get(self,url, params = None, data = None, stream = None):
      return self.request.get(f"{self.baseUrl}/{url}", headers = self.headers, params = params, data = data, stream = stream)


    def post(self, url, params = None, data = None, files = None):
        return self.request.post(f"{self.baseUrl}/{url}", 
                         headers = self.headers, 
                         params = params, 
                         data = data,
                         files=files
                         )
    
    def put(self, url, params = None, data = None, files = None):
        return self.request.put(f"{self.baseUrl}/{url}", 
                         headers = self.headers, 
                         params = params, 
                         data = data,
                         files=files
                         )





    