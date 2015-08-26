from parse_rest.datatypes import Object
from parse_rest.user import User


class Post(Object):
    textLength = 500

    def valid(self):
        return (
            len(self.text or "") > 0 and
            len(self.text or "") < Post.textLength
        )
    
    # text: str
    # author: User
    # voted_user: [User]
