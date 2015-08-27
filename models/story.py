from models.model import Model
from parse_rest.connection import ParseBatcher
from models.post import Post

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
        if len(self.accepted_posts) == 0:
            post_time = self.createdAt
        else:
            post = Post.get(self.accepted_posts[-1]['objectId'])
            post_time = post.createdAt
    
        return (datetime.datetime.now() - post_time)
        
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
        
    def last_update(self):
        if len(self.accepted_posts) == 0:
            return self.createdAt
        else:
            post = Post.get(self.accepted_posts[-1]['objectId'])
            return post.createdAt
        
    def complete(self):
        return len(self.accepted_posts) == Story.max_post_count
        
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
