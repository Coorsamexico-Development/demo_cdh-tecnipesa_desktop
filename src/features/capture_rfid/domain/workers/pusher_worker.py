from PyQt6.QtCore import   QObject
import json
from services.pusher_service import PusherService
import sqlite3
from features.database.managers.sqlite_manager import SqliteManager
from features.capture_rfid.infrastructure.models.tarima_model import TarimaModel
from features.database.models.tarima import Tarima


class PusherWorker(QObject):

    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('database.sqlite')
        self.pusher:PusherService = PusherService(connect_handler=self.connect_handler, show_logging=True)


    def connect_handler(self,_):
        channel = self.pusher.listen("RefreshTarimas")
        channel.bind('App\\Events\\TarimaEvent', self.handle_event)
        # channel.bind('TarimaEvent', self.handle_event)

    def handle_event(self, event_data):
        data_json = json.loads(event_data)
        print(data_json)
        if 'tarima' in data_json and data_json['tarima'] is not None:
            tarima = TarimaModel.fromJson(data_json['tarima'])
            self.updateOrCreate(tarima)

    def start(self):
        self.pusher.connect()


    def updateOrCreate(self, tarima:TarimaModel = None ):

        tarimaDB:Tarima = Tarima.select('*', _connect = self.conn)

        try:
            tarimaDB =  tarimaDB.find(tarima.id)
            if tarimaDB is None:
               tarimaDB = Tarima.create(
                    _connection = self.conn,
                    id=  tarima.id,
                    lpn  = tarima.lpn,
                    token_tag =  tarima.token_tag,
                    switch =  tarima.switch,
                    created_at =   tarima.created_at,
                    updated_at=  tarima.updated_at,
               )
            else:
                tarimaDB.token_tag = tarima.token_tag
                tarimaDB.switch = tarima.switch
                tarimaDB.updated_at = tarima.updated_at
                tarimaDB.save()

        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)


