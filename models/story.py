from models.model import Model
from parse_rest.connection import ParseBatcher
from models.post import Post
from parse_rest.user import User

from parse_rest.connection import SessionToken

import datetime
import time


class Story(Model):
    # Class Properties
    max_post_count = 10
    editing_window = 300  # sec (5 min)
    
    # Properties
    # title: str
    # accepted_posts: [Post]
    # snippets: [Post]

    # Class Accessors
    @classmethod
    def active_story(cls):
        stories = cls.Query.all().order_by("createdAt", descending=True)
        stories = [
            story for story in stories
            if len(story.accepted_posts) < Story.max_post_count
        ]
        
        return cls.get(stories[0].objectId)
        
    # Accessors
    def elapsed_time(self):    
        return (self.updatedAt - datetime.datetime.now())
        
    # ... voting
    def time_til_voting(self):
        seconds = Story.editing_window - self.elapsed_time().seconds
        if seconds < 0:
            return "00:00"
        
        return "%02d:%02d" % divmod(divmod(seconds, 3600)[-1], 60)
    
    def accepting_snippets(self):
        return self.elapsed_time().total_seconds() > Story.editing_window
  
    # ... contributions  
    def contributors(self):
        return set([
            Post.get(p['objectId']).author
            for p in self.accepted_posts
        ])
        
    def complete(self):
        return len(self.accepted_posts) == Story.max_post_count
        
    def user_voted(self, session):
        with SessionToken(session):
            for snippet in self.snippets:
                post = Post.get(snippet['objectId'])
                user_voted = bool([
                    user for user in post.voted_users
                    if user['objectId'] == User.current_user().objectId
                ])
                
                if user_voted:
                    return True
            return False
        
    # Mutators
    def accept_post(self, post):
        snippet_posts = [Post.get(snip['objectId']) for snip in self.snippets]
        for snippet_post in snippet_posts:
            snippet_post.archived = True
            snippet_post.original_story = self
            
        batcher = ParseBatcher()
        batcher.batch_save(snippet_posts)
    
        self.snippets = []
        self.accepted_posts.append(post)
