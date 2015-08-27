from routes.route import Route, require_session
import models

from parse_rest.user import User

import flask


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
        
        return flask.redirect('/', 200)
        

class Vote(Route):
    methods = ['POST']
    
    @require_session
    def POST(self, request, post_id):
        story = models.story.Story.active_story()
        if not story:
            return ("", 400)
        elif not story.accepting_snippets():
            return ("", 429)
            
        post = models.post.Post.get(post_id)
        if not post:
            return ("", 404)
            
        voted_users = set(post.voted_users)
        voted_users.add(User.current_user())
        
        post.voted_users = list(voted_users)
        post.save()
        
        if len(post.voted_users) >= models.post.Post.max_vote_count():
            story.accept_post(post)
            story.save()
        
        return flask.redirect('/', 200)
