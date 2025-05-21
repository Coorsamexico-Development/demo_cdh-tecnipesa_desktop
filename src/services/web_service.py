import asyncio
from flask import Flask
from flask import request
import json
from services.websocket_service import WebsocketService



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

# @flask_app.put('/api/v1/device/gpos')
# def update_gpos():
#     # Enviar mensaje a todos los WebSocket conectados
#     data =request.data
#     return "Exitoso"




def run_flask():
    flask_app.run(host="0.0.0.0",port=5000)
