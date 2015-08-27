from parse_rest.user import User
from models.model import Model


class Post(Model):
    # Class Properties
    textLength = 500
    
    # Properties
    # text: str
    # author: User
    # voted_users: [User]
    # archived: bool

    # Class Accessors
    @classmethod
    def max_vote_count(cls):
        return 2

    # Accessors
    def valid(self):
        return (
            len(self.text or "") > 0 and
            len(self.text or "") < Post.textLength
        )
        
# Functions
def comparePosts(self, other):
    if len(other.voted_users) > len(self.voted_users):
        return 1
    elif len(self.voted_users) > len(other.voted_users):
        return -1
    
    if other.createdAt > self.createdAt:
        return 1
    else:
        return -1

    