import os
from sqlite3 import Cursor, Error


from features.database.managers.sqlite_manager import SqlliteManager

class QueryMigration:
    def __init__(self, query:str,check_table_exist:bool=False, table = '' ) -> None:
        self.sql_query = query
        
        self.check_table_exist = check_table_exist
        self.table = table

        def __str__(self):
            return self.sql_query
        


class Migration:
    def __init__(self, querys: list[QueryMigration]=[]) -> None:
        self.db_manager = SqlliteManager()
        self.querys = querys

    def up(self):
        if not os.path.exists(self.db_manager.db_file):
            with open(self.db_manager.db_file, 'w') as _:
                pass
            
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        for query in self.querys:
            try:
                if query.check_table_exist:
                    if self.table_exists(cursor=cursor,table_name= query.table):
                        continue

                cursor.execute(query.sql_query)
                print(f"Success created table: {query.table}")
            except Error as e:
                print(e)
                print("Error created table: " +query.table )        

        conn.commit()
        cursor.close()
        print(self.db_manager.db_file)

     # Función para verificar si una tabla existe
    def table_exists(self,cursor:Cursor, table_name:str):
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
        return cursor.fetchone() is not None