import json


class TagInventory:
    def __init__(self,epc:str, antenna_port:int, peak_rssi_cdbm:int, frequency:int, transmit_power_cdbm:int
                    ):
        self.epc = epc
        self.antenna_port = antenna_port
        self.peak_rssi_cdbm = peak_rssi_cdbm
        self.frequency = frequency
        self.transmit_power_cdbm = transmit_power_cdbm

    def to_dict(self):
        return {
            'epc': self.epc,
            'antenna_port': self.antenna_port,
            'peak_rssi_cdbm': self.peak_rssi_cdbm,
            'frequency': self.frequency,
            'transmit_power_cdbm': self.transmit_power_cdbm,
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def to_dict_str(self):
        return self.to_dict()

    
    def __str__(self):
        return f'TagInventory: {self.to_json()}'
    
    def __repr__(self):
        return f"TagInventory({self.epc})"