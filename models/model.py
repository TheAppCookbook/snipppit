from parse_rest.datatypes import Object
from parse_rest.query import QueryResourceDoesNotExist


class Model(Object):
    # Class Accessors
    @classmethod
    def get(cls, id):
        try:
            return cls.Query.get(objectId=id)
        except QueryResourceDoesNotExist:
            return None
