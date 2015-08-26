from routes.route import Route
from models.story import Story
import flask

class Post(Route):
    methods = ['PUT']
    
    def PUT(self, request):
        return "ADD POST"
        

class Vote(Route):
    methods = ['PUT']
    
    def PUT(self, request, post_id):
        return "ADD VOTE TO " + post_id
