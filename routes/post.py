from routes.route import Route, require_session
import models

from parse_rest.user import User

import flask
import json


class Post(Route):
    methods = ['POST']
    
    @require_session
    def POST(self, request):
        story = models.story.Story.active_story()
        if not story:
            return ("Cannot find active story", 400)
            
        post = models.post.Post(
            text=request.values.get("text"),
            author=User.current_user(),
            voted_users=[],
            archived=False
        )
        
        if not post or not post.valid():
            return ("Post invalid " + str(post), 400)
            
        post.save()
        
        story.snippets.append(post)
        story.save()
        
        return flask.redirect('/')
        

class Vote(Route):
    methods = ['PUT', 'DELETE']
    
    @require_session
    def PUT(self, request, post_id):
        story = models.story.Story.active_story()
        if not story:
            return ("", 400)
        elif not story.accepting_snippets():
            return ("", 429)
            
        post = models.post.Post.get(post_id)
        if not post:
            return ("", 404)
            
        voted_users = [user['objectId'] for user in post.voted_users]
        if User.current_user().objectId not in voted_users:
            post.voted_users.append(User.current_user())
        
        post.save()
        
        refresh = False
        if len(post.voted_users) >= models.post.Post.max_vote_count():
            story.accept_post(post)
            story.save()
            
            refresh = True
        
        return json.dumps({
            'votes': len(post.voted_users),
            'refresh': refresh
        })
        
    @require_session
    def DELETE(self, request, post_id):
        story = models.story.Story.active_story()
        if not story:
            return ("", 400)
        elif not story.accepting_snippets():
            return ("", 429)
            
        post = models.post.Post.get(post_id)
        if not post:
            return ("", 404)
            
        voted_users = [user['objectId'] for user in post.voted_users]
        if User.current_user().objectId in voted_users:
            post.voted_users = [
                user for user in post.voted_users
                if user['objectId'] != User.current_user().objectId
            ]
        
        post.save()
        return json.dumps({
            'votes': len(post.voted_users)
        })
