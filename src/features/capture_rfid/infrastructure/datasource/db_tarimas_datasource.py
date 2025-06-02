from features.capture_rfid.infrastructure.models.tarima_model import TarimaModel
from features.database.models.tarima import Tarima
from sqlite3 import Error
from features.shared.errors.sql_error import SqlError

class DBTarimasDatasource:
    def __init__(self):
        pass

    def updateOrCreate(self, tarima:TarimaModel = None )->Tarima:

        tarimaDB:Tarima = Tarima.select('*')

        try:
            tarimaDB =  tarimaDB.find(tarima.id)
            if tarimaDB is None:
               tarimaDB = self.create(tarima)
            else:
                self.update(tarimaDB=tarimaDB, tarima=tarima)

            return tarimaDB

        except Error as e:
            print(e)
            raise SqlError(title="Error SQL",
                                message="Error update or create Tarima")
        except Exception as e:
            print(e)
            raise SqlError(title="Error SQL",
                                message="Error update or create Tarima")
        
    def create(self, tarima:TarimaModel = None )->Tarima:
        return Tarima.create(
                    id=  tarima.id,
                    lpn  = tarima.lpn,
                    token_tag =  tarima.token_tag,
                    switch =  tarima.switch,
                    created_at =   tarima.created_at,
                    updated_at=  tarima.updated_at,
               )
    
    def update(self,tarimaDB: Tarima, tarima:TarimaModel)->Tarima:
        tarimaDB.token_tag = tarima.token_tag
        tarimaDB.switch = tarima.switch
        tarimaDB.updated_at = tarima.updated_at
        tarimaDB.save()