from routes.route import Route
import models

from parse_rest.connection import ACCESS_KEYS
from parse_rest.user import User

import flask


class Story(Route):
    methods = ['GET', 'PUT']
    
    def GET(self, request, story_id):
        session = request.values.get("session")
        
        story = models.story.Story.get(story_id)
        if not story:
            story = models.story.Story.active_story()
            
        accepted_posts = sorted([
            models.post.Post.get(post['objectId'])
            for post in story.accepted_posts
        ], key="createdAt")
        
        snippets = sorted([
            models.post.Post.get(post['objectId'])
            for post in story.snippets
        ], cmp=models.post.comparePosts)
        
        return flask.render_template(
            "story.html",
            story=story,
            accepted_posts=accepted_posts,
            snippets=snippets,
            session = self.session(request)
        )
        
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
