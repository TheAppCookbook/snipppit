from parse_rest.user import User
from models.model import Model

from parse_rest.connection import SessionToken



class Post(Model):
    # Class Properties
    text_length = 500
    
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
            len(self.text or "") < Post.text_length
        )
        
    def user_voted(self, session):
        with SessionToken(session):        
            return bool([
                user for user in self.voted_users
                if user['objectId'] == User.current_user().objectId
            ])
    
    def author_initials(self):
        initials = ":)"
        
        user = self.author
        if user:
            initials = user.first_name[0] + user.last_name[0]
            
        return initials
        
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

    