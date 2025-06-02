from typing import Union
from features.capture_rfid.infrastructure.models.tarima_model import TarimaModel

class TarimaPaginationModel:
    def __init__(self,
                 current_page:int, 
                 data:list[TarimaModel], 
                 first_page_url:str,
                 from_page:Union[int, None], 
                 next_page_url:Union[str, None],
                 path:str,
                 per_page:int,
                 prev_page_url:Union[str, None],
                 to:Union[int, None]):
        self.current_page = current_page
        self.data = data
        self.first_page_url = first_page_url
        self.from_page = from_page
        self.next_page_url = next_page_url
        self.path = path
        self.per_page = per_page
        self.prev_page_url = prev_page_url
        self.to = to