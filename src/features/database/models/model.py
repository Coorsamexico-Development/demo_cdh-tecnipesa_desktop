from datetime import datetime
from features.database.managers.sqlite_manager import SqlliteManager
from features.database.models.collection_db import CollectionDB
from features.database.utils.convertions import create_slug
from sqlite3 import Connection
from typing import Union

base_atributes = [
    'primary_key',
    'table',
    '_exist',
    '_connection'
]
class Model:
    
    def __init__(self, **kwargs):
        table_name = create_slug(self.__class__.__name__) + 's'
        self._attributes = {
            'primary_key' :'id',
            'table': table_name,
            '_exist': False
        }
        self._original_attributes = {
            'primary_key' :'id',
            'table': table_name,
            '_exist': False
        }
        self._connection:Union[Connection,None] = None
        for key, value in kwargs.items():
            if key == '_connection':
                self._connection = value
                continue
            self._attributes[key] = value
            self._original_attributes[key] = value
        if self._connection is None:
            self._connection = SqlliteManager().get_connection()
            

    def __setattr__(self, name, value):
        
        if name in ('_attributes', '_original_attributes'):
            super().__setattr__(name, value)
        else:
            self._attributes[name] = value
            

            

    def __getattr__(self, name):
        if name in self._attributes:
            return self._attributes[name]
        raise AttributeError(f"'{type(self)._name_}' object has no attribute '{name}'")


    def getOriginal(self, key=None):
        # Return only the original attributes
        if key is None:
           return self._attributes[key]
        return {key: value for key, value in self._original_attributes.items() if value is not None}
    
    def isDirty(self, key=None)->bool:
        # Return True if any attributes was changed of original attributes
        if key is not None: 
           if key not in self._original_attributes:
               return True
           return self._original_attributes[key] != self._attributes[key]
        for key,value in  self._attributes:
            if self._original_attributes[key] != value:
                return True
        return False
    
    def getDirty(self):
        dirty = {}
        for key, value in self._attributes.items():
            if key not in self._original_attributes or self._original_attributes[key] != self._attributes[key]:
                dirty[key] = value
        
        return dirty

    

    
    def insert_db(self):
        cursor = self._connection.cursor()
        start_time = datetime.now()
        if 'created_at' not in self._attributes:
            self._attributes['created_at'] = start_time.strftime("%Y/%m/%d %H:%M:%S")
        if 'updated_at' not in self._attributes:
            self._attributes['updated_at'] = start_time.strftime("%Y/%m/%d %H:%M:%S")
        
        
        params = {key: value for key, value in self._attributes.items() if key not in base_atributes}
        
        columns_names = ", ".join([f"`{key}`" for key in params.keys() ])
        columns_signs = ", ".join(['?' for _ in params.keys()])



        query_insert = f"INSERT INTO `{self.table}`({columns_names}) VALUES ({columns_signs})"
        values = tuple(params.values())
        cursor.execute(query_insert, values)
        self._attributes['id'] = cursor.lastrowid
        self._attributes['_exist'] = True
        self._connection.commit()
        cursor.close()

    def update_db(self, where=None):
        cursor = self._connection.cursor()
        if where is None:
            where = f"WHERE {self.primary_key} = {self._attributes[self.primary_key]}"

        params = self.getDirty()
        if len(params) > 0:
            if not self.isDirty('updated_at'):
                start_time = datetime.now()
                params['updated_at'] = start_time.strftime("%Y/%m/%d %H:%M:%S")

        params = {key: value for key, value in params.items() if key not in base_atributes}
        if not params:
            return

        columns_update = ", ".join([f'{key} = ?' for key in params.keys()])
      

        query_update = f"UPDATE `{self.table}` SET {columns_update} {where}"
        cursor.execute(query_update, tuple(params.values()))
        self._connection.commit()
        cursor.close()

    def delete(self)->int:
        cursor = self._connection.cursor()
        where = f"WHERE {self.primary_key} = ?"
        query_delete = f"DELETE FROM `{self.table}` {where}"
        cursor.execute(query_delete, tuple([self._attributes[self.primary_key]]))
        affected = cursor.rowcount
        self._connection.commit()
        cursor.close()
        self._exist = False
        return affected

    
    
    def save(self):
        if self._exist:
            self.update_db()
        else:
            self.insert_db()

    
    @classmethod
    def create(cls,**kwargs):
        instance = cls(**kwargs)
        instance.save()
        return instance
    @classmethod
    def select(cls, *selects):
        return CollectionDB(cls).select(*selects)
    
    @classmethod
    def selectRaw(cls, select_text:str):
        return CollectionDB(cls).selectRaw(select_text)
    

    @classmethod
    def find(cls, value):
        return CollectionDB(cls).find(value)

