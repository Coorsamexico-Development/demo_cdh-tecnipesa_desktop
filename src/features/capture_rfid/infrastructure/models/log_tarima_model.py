
import json

class LogTarimaModel:
    def __init__(self, id:int, tarima_id:int, fecha_movimiento:str, sentido: str
                    ):
        self.id = id
        self.tarima_id = tarima_id
        self.fecha_movimiento = fecha_movimiento
        self.sentido = sentido

    #make a to dict method
    def to_dict(self):
        return {
            'id': self.id,
            'tarima_id': self.tarima_id,
            'fecha_movimiento': self.fecha_movimiento,
            'sentido': self.sentido,
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def to_dict_str(self):
        return self.to_dict()

    
    def __str__(self):
        return f'LogTarima: {self.to_json()}'
    
    def __repr__(self):
        return f"LogTarimaModel({self.id})"