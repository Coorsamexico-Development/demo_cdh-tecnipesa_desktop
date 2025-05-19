import base64
from features.capture_rfid.infrastructure.models.scaneo_model import ScaneoModel
from features.capture_rfid.infrastructure.models.tag_inventory import TagInventory

class ScaneoAdapter: 
    @staticmethod
    def fromJson(dict): 
        
        return ScaneoModel(
            timestamp= dict['timestamp'],
            event_type=dict['eventType'],
            tag_inventory_event=TagInventory(
                epc=base64.urlsafe_b64decode(dict['tagInventoryEvent']["epc"]).hex().upper(),
                antenna_port=dict['tagInventoryEvent']["antennaPort"],
                peak_rssi_cdbm=dict['tagInventoryEvent']["peakRssiCdbm"],
                frequency=dict['tagInventoryEvent']["frequency"],
                transmit_power_cdbm=dict['tagInventoryEvent']["transmitPowerCdbm"],
            ),
        )
    