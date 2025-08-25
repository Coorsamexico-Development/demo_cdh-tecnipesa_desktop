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
            anntena_port =  randint(1, 8)

            epcs = ["4oARkaUDAGXybMv_", "4oARkaUDAGXybNAf"]


            data = {
                "timestamp": "2025-05-17T16:03:13.944189383Z",
                "eventType": "tagInventory",
                "tagInventoryEvent": {
                    "epc": epcs[anntena_port % 2],
                    "antennaPort": anntena_port,
                    "peakRssiCdbm": -7300,
                    "frequency": 919750,
                    "transmitPowerCdbm": 3000
                }
            }
            yield json.dumps(data) + "\n"
            time.sleep(0.300)
            if anntena_port == 8:
                print("<------- FINISH STREAM--->")
                break
    return Response(generate(), mimetype='text/event-stream')


@flask_app.post('/api/v1/logtarima')
def storeLogtarima():
    # Enviar mensaje a todos los WebSocket conectados

    colors = ["blue","green","red", "blue"]
    color =  colors[randint(0, len(colors)-1)]
    data =request.form
    print(f"Color response: {color}, data: {data}")

    return {
        "data": {
            "color": color,

        }
    }
@flask_app.get('/api/v1/tarima')
def getTarimas():
    # Enviar mensaje a todos los WebSocket conectados

    # colors = ["blue","green","red", "blue"]
    # color =  colors[randint(0, len(colors)-1)]
    # data =request.form
    # print(f"Color response: {color}, data: {data}")
    data =request.get_json()

    print(f"tarima api: {data}")

    return {

        "current_page": 1,
        "data": [],
        "first_page_url": "/api/v1/tarima",
        "from_page": 1,
        "next_page_url": None,
        "path": "tarima",
        "per_page": 100,
        "prev_page_url": None,
        "to": None,
    }



def run_flask():
    flask_app.run(host="0.0.0.0",port=5001)
