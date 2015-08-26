from routes.route import Route
import models

from parse_rest.connection import ACCESS_KEYS

import flask


class Story(Route):
    methods = ['GET', 'PUT']
    
    def GET(self, request, story_id):
        session = request.values.get("session")
        return flask.render_template("story.html")
        
    def PUT(self, request, story_id):
        auth_token = request.values.get("auth_token")
        if auth_token != ACCESS_KEYS['rest_key']:
            return ("", 401)
        
        story = models.story.Story(
            title=request.values.get("title"),
            accepted_posts = [],
            snippets = []
        )
        
        story.save()        
        return story.title + " saved (" + story.objectId + ")"

    
class Stories(Route):
    methods = ['GET']
    
    def GET(self, request):
        return "VIEW STORIES LIST"
