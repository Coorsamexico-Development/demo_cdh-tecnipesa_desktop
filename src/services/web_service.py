import asyncio
from flask import Flask,Response
from flask import request
import json
from services.websocket_service import WebsocketService
from PyQt6.QtCore import pyqtSignal, QObject
import time
from random import randint
class Communicator(QObject):
    message_received = pyqtSignal(str)

communicator = Communicator()


flask_app = Flask(__name__) 
    
# --- Flask App ---

@flask_app.post('/api/v1/webhook')
def webhook():
    # Enviar mensaje a todos los WebSocket conectados
    dataJson =request.get_json()

    if not dataJson:
        return "" 
    
    if len(dataJson) == 0:
        return
    asyncio.run(WebsocketService.send_ws_message(json.dumps(dataJson)))
    return "Exitoso"

@flask_app.put('/api/v1/device/gpos')
def update_gpos():
    # Enviar mensaje a todos los WebSocket conectados
    data =request.data
    print(f"set colors gpos: {data}")
    return "Exitoso"


@flask_app.get('/api/v1/data/stream')
def stream():
    # Enviar mensaje a todos los WebSocket conectados
    def generate():
        while True:
            data = {
                "timestamp": "2025-05-17T16:03:13.944189383Z",
                "eventType": "tagInventory",
                "tagInventoryEvent": {
                    "epc": "4oARkaUDAGXybMv_",
                    "antennaPort": 1,
                    "peakRssiCdbm": -7300,
                    "frequency": 919750,
                    "transmitPowerCdbm": 3000
                }
            }
            yield json.dumps(data) + "\n"
            time.sleep(1)
    return Response(generate(), mimetype='text/event-stream')


@flask_app.post('/api/v1/logtarima')
def storeLogtarima():
    # Enviar mensaje a todos los WebSocket conectados

    colors = ["yellow","green","red", "yellow"]
    color =  colors[randint(0, len(colors)-1)]
    print(f"color response: {color}")

    return {
        "data": {
            "color": color
        }
    }



def run_flask():
    flask_app.run(host="0.0.0.0",port=5001)
