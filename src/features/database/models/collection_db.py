from typing import Union
from features.database.managers.sqlite_manager import SqlliteManager


class CollectionDB:
    

    def __init__(self, cls, query: str = 'SELECT [selects] FROM `[table]` [joins] [wheres] [groups] [orderBy] [limits]'):
        self.cls = cls
        instnace = cls()
        self.query = query
        self.table = instnace.table
        self.primary_key = instnace.primary_key
        self._connection = instnace._connection
        self.selects = '*'
        self.query_limit = ''
        self.query_groups= ''
        self.query_where = ''
        self.query_order_by = ''
        self.query_joins = ''
        self.query_values = []

    def select(self,*selects):
        select_txt = ','.join(select for select in selects)
        self.selects = select_txt
        return self
    
    def selectRaw(self,select_txt:str):
        self.selects = select_txt
        return self
    
    def innerJoin(self,table:str, column1:str, operator:str, column2:str):
        self.query_joins = f"INNER JOIN {table} ON {column1} {operator} {column2} "
        return self


    def whereRaw(self,query_raw:str):
        self.query_where = query_raw
        return self

    def where(self,column:str, valueOrOperator:str, value:Union[str, None] = None):
        self.whereQuery(column=column, valueOrOperator=valueOrOperator, value=value)
        return self
    

    def orWhere(self,column:str, valueOrOperator:str, value:Union[str, None] = None):
        self.whereQuery(column=column, valueOrOperator=valueOrOperator, value=value, sql_operator='OR')
        return self



    def whereQuery(self,column:str, valueOrOperator:str, value:Union[str, None] = None, sql_operator = 'AND'):
        query_where = self.query_where
        if not self.query_where :
            query_where = 'WHERE '
        else:
             query_where += f" {sql_operator} "
        operator = '='
        #actua como operador
        if value is not None:
            operator = valueOrOperator
        else:
            value = valueOrOperator
        query_where += f'{column} {operator} ?'
        self.query_where = query_where
        self.query_values.append(value)
        return self
    


    def limit(self, value:int):
        self.query_limit = f'limit {value}'
        return self
    
    def orderBy(self, column:str, order:str= 'asc'):
        self.query_order_by = f'order by {column} {order}'
        return self
    
    def groupBy(self,*columns):
        group_txt = ','.join(column for column in columns)
        self.query_groups = "GROUP BY" +  group_txt
        return self
    


    def limit(self, value:int):
        self.query_limit = f'limit {value}'
        return self

    def get(self):
        list_intances = self._excute_query()
        return list_intances
    
    def find(self, value):
        self.query_where = f'WHERE `{self.table}`.`{self.primary_key}` = ?'
        self.query_values.append(value)
        return self.first()
    

    def first(self):
        self.query_limit = 'LIMIT 1'
        list_intances = self._excute_query()
        if len(list_intances) > 0:
            return list_intances[0]
        return None
    
    def firstWhere(self,column:str, valueOrOperator:str, value:Union[str, None] = None):
        self.whereQuery(column=column, valueOrOperator=valueOrOperator,value=value)
        return self.first()
        
    
    def _colums_query(self, cursor):
        columnas = [description[0] for description in cursor.description]
        return columnas
    

    def _excute_query(self)->list:
        cursor = self._connection.cursor()
        self.set_querys()
        # print(f"{self.query} ({self.query_values})")
        cursor.execute(self.query, tuple(self.query_values))
        rows = cursor.fetchall()
        columnas = self._colums_query(cursor)
        list_intances = []
        for row in rows:
            params = {'_exist': True}
            for i,value in enumerate(row):
                params[columnas[i]] = value

            list_intances.append(self.cls(**params))
        cursor.close()
    

        return list_intances

    
    def set_querys(self):
        replace_sentence = {
            '[selects]' : self.selects,
            '[table]' : self.table,
            '[joins]' : self.query_joins,
            '[wheres]' : self.query_where,
            '[groups]' : self.query_groups,
            '[orderBy]': self.query_order_by,
            '[limits]' : self.query_limit,
        }
        new_query = self.query
        for old, new in replace_sentence.items():
            new_query = new_query.replace(old, new)
        self.query = new_query





    