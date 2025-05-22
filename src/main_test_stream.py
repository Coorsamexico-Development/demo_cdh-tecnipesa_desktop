from requests.exceptions import ConnectTimeout
from services.api_impinj_service import api_impinj
from features.shared.errors.request_error import RequestError

try:
    with api_impinj.get('data/stream', stream=True) as response:
        for line in response.iter_lines():
            if line:
                print(line.decode('utf-8'))
                print("-------------------------------------------------")
    
except ConnectTimeout as e:
    print(RequestError(title="Sin conexion a la api",
                        message="LLevo mucho tiempo la solicitud al servidor asegurate de tener conexicón a Internet", 
                        code=500))
except RequestError as e:
    print(e)
except Exception as e:
    print(RequestError(title="Error",
                        message="Problemas con la API", 
                        code=500))