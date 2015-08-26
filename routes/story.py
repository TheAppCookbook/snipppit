from routes.route import Route
from models.story import Story
import flask

class Story(Route):
    methods = ['GET']
    
    def GET(self, request, story_id):
        return "VIEW STORY PAGE " + str(story_id)

    
class Stories(Route):
    methods = ['GET']
    
    def GET(self, request):
        return "VIEW STORIES LIST"