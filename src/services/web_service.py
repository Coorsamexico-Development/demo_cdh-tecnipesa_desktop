import asyncio
from flask import Flask
from flask import request
import json
from services.websocket_service import WebsocketService



flask_app = Flask(__name__) 
    
# --- Flask App ---

@flask_app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # Enviar mensaje a todos los WebSocket conectados
    dataJson =request.get_json()

    if not dataJson:
        return "" 
    
    if len(dataJson) == 0:
        return
    asyncio.run(WebsocketService.send_ws_message(json.dumps(dataJson)))
    return "Exitoso"


def run_flask():
    flask_app.run(host="0.0.0.0",port=5000)
