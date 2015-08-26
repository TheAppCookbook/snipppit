from parse_rest.datatypes import Object


class Story(Object):
    max_post_size = 10

    @classmethod
    def active_story(cls):
        stories = cls.Query.all().order_by("createdAt", descending=True)    
        stories = [
            story for story in stories
            if len(story.accepted_posts) < Story.max_post_size
        ]
        
        return stories[0]
        
    
    # title: str
    # accepted_posts: [Post]
    # snippets: [Post]
