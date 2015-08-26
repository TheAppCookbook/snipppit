from routes.route import Route
import flask

class Index(Route):
    methods = ['GET']
    
    def GET(self, request):
        return "REDIR TO /story/active"