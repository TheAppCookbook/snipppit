from parse_rest.connection import SessionToken
from parse_rest.core import ResourceRequestNotFound


class Route:
    methods = []
    
    def route(self, request, *args):
        if request.method == 'GET':
            return self.GET(request, *args) 
        elif request.method == 'POST':
            return self.POST(request, *args)
        elif request.method == 'PUT':
            return self.PUT(request, *args)
        elif request.method == 'DELETE':
            return self.DELETE(request, *args)

def require_session(func):
    def func_wrapper(self, request, *args):
        try:
            session = request.values.get('session')
            with SessionToken(session):
                 return func(self, request, *args)
        except ResourceRequestNotFound:
            pass
             
        return ("", 401)
        
    return func_wrapper