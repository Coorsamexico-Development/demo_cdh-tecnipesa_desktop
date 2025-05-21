
import json
from features.capture_rfid.infrastructure.models.tag_inventory import TagInventory



class ScaneoModel:
    def __init__(self, timestamp:str, event_type:str, tag_inventory_event:TagInventory
                    ):
        self.timestamp = timestamp
        self.event_type = event_type
        self.tag_inventory_event = tag_inventory_event
        self.image = None

    #make a to dict method
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'event_type': self.event_type,
            'tag_inventory_event': self.tag_inventory_event.to_dict(),
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def to_dict_str(self):
        return self.to_dict()

    
    def __str__(self):
        return f'Scaneo: {self.to_json()}'
    
    def __repr__(self):
        return f"ScaneoModel({self.timestamp})"