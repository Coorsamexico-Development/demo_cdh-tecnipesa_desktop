from features.database.models.model import Model
import os
import sqlite3
db_file = os.path.join(os.getcwd(), 'assets', 'database', 'database.sqlite')

class TarimaInPusher(Model):
    

    def __init__(self, **kwargs):
        table = 'tarimas'
        _connection = sqlite3.connect(db_file)
        super().__init__(table=table, _connection=_connection,**kwargs)