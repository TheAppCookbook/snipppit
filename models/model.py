from parse_rest.datatypes import Object
from parse_rest.query import QueryResourceDoesNotExist

import datetime


class Model(Object):
    # Class Accessors
    @classmethod
    def get(cls, id):
        try:
            return cls.Query.get(objectId=id)
        except QueryResourceDoesNotExist:
            return None
    
    @classmethod
    def all(cls):
        return cls.Query.all().order_by("createdAt", descending=True)
        
    # Accessors
    def elapsed_time(self):
        return (self.createdAt - datetime.datetime.now())