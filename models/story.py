from parse_rest.datatypes import Object
from parse_rest.connection import ParseBatcher
from models.post import Post

import datetime


class Story(Object):
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
            if len(story.accepted_posts) < Story.max_post_size
        ]
        
        return stories[0]
        
    # Accessors
    def accepting_snippets(self):
        if len(self.accepted_posts) == 0:
            post_time = self.createdAt
        else:
            post_time = self.accepted_posts[-1].createdAt
            
        elapsed_time = (datetime.now - self.createdAt).total_seconds()
        return elapsed_time > Story.editing_window
        
    def complete(self):
        return len(self.accepted_posts) == Story.max_post_count
        
    # Mutators
    def accept_post(self, post):
        for snippet_post in self.snippets:
            snippet_post.archived = True
            snippet_post.original_story = self
            
        batcher = ParseBatcher()
        batcher.batch_save(self.snippets)
    
        self.snippets = []
        self.accepted_posts.append(post)
