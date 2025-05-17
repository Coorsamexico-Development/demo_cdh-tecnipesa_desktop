
import json
from features.capture_rfid.infrastructure.models.tag_inventory import TagInventory



class ScaneoModel:
    def __init__(self, timestamp:str, eventType:str, tagInventoryEvent:TagInventory
                    ):
        self.timestamp = timestamp
        self.eventType = eventType
        self.tagInventoryEvent = tagInventoryEvent

    #make a to dict method
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'eventType': self.eventType,
            'tagInventoryEvent': self.tagInventoryEvent.to_dict(),
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def to_dict_str(self):
        return self.to_dict()

    
    def __str__(self):
        return f'Scaneo: {self.to_json()}'
    
    def __repr__(self):
        return f"ScaneoModel({self.timestamp})"