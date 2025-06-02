import base64
from features.capture_rfid.infrastructure.models.scaneo_model import ScaneoModel
from features.capture_rfid.infrastructure.models.tag_inventory import TagInventory
from features.capture_rfid.infrastructure.models.tarima_pagination_model import (
    TarimaPaginationModel)
from features.capture_rfid.infrastructure.models.tarima_model import TarimaModel

class TarimaPaginationAdapter: 
    @staticmethod
    def fromJson(dict): 
        return TarimaPaginationModel(
            current_page = dict['current_page'], 
            data= [TarimaModel.fromJson(data) for data in dict['data']], 
            first_page_url= dict['first_page_url'],
            from_page= dict['from'], 
            next_page_url= dict['next_page_url'],
            path= dict['path'],
            per_page= dict['per_page'],
            prev_page_url= dict['prev_page_url'],
            to= dict['to']
        )
    