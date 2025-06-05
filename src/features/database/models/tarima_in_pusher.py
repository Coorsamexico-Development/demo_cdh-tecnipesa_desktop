from features.database.models.model import Model
import sqlite3
from config.resource_path import resource_path
db_file = resource_path( 'assets', 'database', 'database.sqlite')

class TarimaInPusher(Model):
    

    def __init__(self, **kwargs):
        table = 'tarimas'
        _connection = sqlite3.connect(db_file)
        super().__init__(table=table, _connection=_connection,**kwargs)