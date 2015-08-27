from routes.route import Route
import models

from parse_rest.connection import SessionToken
from parse_rest.connection import ACCESS_KEYS
from parse_rest.user import User

import flask


class Story(Route):
    methods = ['GET', 'PUT']
    
    def GET(self, request, story_id):        
        story = models.story.Story.get(story_id)
        if not story:
            story = models.story.Story.active_story()
            
        accepted_posts = sorted([
            models.post.Post.get(post['objectId'])
            for post in story.accepted_posts
        ], cmp=lambda x, y: 1 if x.createdAt > y.createdAt else -1)
        
        snippets = sorted([
            models.post.Post.get(post['objectId'])
            for post in story.snippets
        ], cmp=models.post.comparePosts)
        
        initials = ":)"
        if self.session(request):
            with SessionToken(self.session(request)):
                user = User.current_user()
                initials = user.first_name[0] + user.last_name[0]
        
        return flask.render_template(
            "story.html",
            story=story,
            accepted_posts=accepted_posts,
            snippets=snippets,
            
            initials = initials,
            session = self.session(request),
            
            max_vote_count=models.post.Post.max_vote_count(),
            user_voted_story=story.user_voted(self.session(request)),
            
            text_length=models.post.Post.text_length
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
        number_of_columns_per_row = 3
    
        stories = models.story.Story.all()
        rows = []
        
        row = []
        for story in stories:
            if len(story.accepted_posts) > 0:
                post = models.post.Post.get(story.accepted_posts[-1]['objectId'])
                preview = post.text
            else:
                preview =  None
            row.append((story, preview))

            if len(row) == number_of_columns_per_row:
                rows.append(row)
                row = []
        rows.append(row)
                
        print(stories)
        return flask.render_template(
            "browse.html",
            rows=rows
        )
