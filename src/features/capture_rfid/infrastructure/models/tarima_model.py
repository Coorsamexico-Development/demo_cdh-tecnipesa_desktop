# from datetime import datetime
import json
from typing import Union

class TarimaModel:
    def __init__(self,
                 id:int, 
                 lpn:str, 
                 token_tag:str, 
                 switch:int, 
                 created_at:Union[str, None],
                 updated_at:Union[str, None]
                    ):
        self.id = id
        self.lpn = lpn
        self.token_tag = token_tag
        self.switch = switch
        self.created_at = created_at
        self.updated_at = updated_at
        

    def to_dict(self):
        return {
            'id': self.id,
            'lpn': self.lpn,
            'token_tag': self.token_tag,
            'switch': self.switch,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def to_dict_str(self):
        return self.to_dict()

    
    def __str__(self):
        return f'TarimaModel: {self.to_json()}'
    
    def __repr__(self):
        return f"TarimaModel({self.id})"
    

    @classmethod
    def fromJson(cls, json):
        created_at = None
        updated_at = None
        if 'created_at' in json:
            # created_at = datetime.strptime(json["created_at"], "%Y-%m-%d %H:%M:%S")
            created_at = json["created_at"]
       
        if 'updated_at' in json:
            # updated_at = datetime.strptime(json["updated_at"], "%Y-%m-%d %H:%M:%S")
            updated_at = json["updated_at"]
        return cls(
                id=json['id'], 
                lpn=json['lpn'], 
                token_tag=json['token_tag'], 
                switch=json['switch'], 
                created_at=created_at,
                updated_at=updated_at
                )
    