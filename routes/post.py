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
            return ("", 400)
            
        post = models.post.Post(
            text=request.values.get("text"),
            author=User.current_user()
        )
        
        if not post or not post.valid():
            return ("", 400)
            
        post.save()
        
        story.snippets.append(post)
        story.save()
        
        return flask.redirect('/', 200)
        

class Vote(Route):
    methods = ['POST']
    
    @require_session
    def POST(self, request, post_id):
        return "ADD VOTE TO " + post_id
