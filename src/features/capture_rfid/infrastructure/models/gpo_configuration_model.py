from enum import Enum
import json


class GpoConfigurationModel:

    class StateGeo(Enum):
        HIGH = "high"
        LOW = "low"

    def __init__(self, gpo:int, state:StateGeo):
        self.gpo = gpo
        self.state = state

    #make a to dict method
    def to_dict(self):
        return {
            'gpo': self.gpo,
            'state': self.state.value
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def to_dict_str(self):
        return self.to_dict()

    
    




