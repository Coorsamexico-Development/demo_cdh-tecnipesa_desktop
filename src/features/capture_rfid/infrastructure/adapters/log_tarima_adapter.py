
from features.capture_rfid.infrastructure.models.log_tarima_model import LogTarimaModel

class LogTarimaAdapter: 
    @staticmethod
    def fromJson(dict): 
        
        return LogTarimaModel(
            id= dict['id'],
            tarima_id= dict['tarima_id'],
            fecha_movimiento= dict['fecha_movimiento'],
            sentido= dict['sentido']
        )
    