import requests


class RequestService():
    def __init__(self, baseUrl = '', headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
    ):
        super().__init__()
        self.baseUrl = baseUrl
        self.headers = headers




    def get(self,url, params = None, data = None):

      return requests.get(f"{self.baseUrl}/{url}", headers = self.headers, params = params, data = data)


    def post(self, url, params = None, data = None, files = None):
        return requests.post(f"{self.baseUrl}/{url}", 
                         headers = self.headers, 
                         params = params, 
                         data = data,
                         files=files
                         )
    
    def put(self, url, params = None, data = None, files = None):
        return requests.put(f"{self.baseUrl}/{url}", 
                         headers = self.headers, 
                         params = params, 
                         data = data,
                         files=files
                         )








    