from commons import parse_client
from parse_rest.datatypes import Object as ParseObject
from parse_rest.user import User


class Post(ParseObject):
    textLength = 500

    def valid(self):
        return (
            len(self.text or "") > 0 and
            len(self.text or "") < Post.textLength
        )
    
    # text: str
    # author: User
    # voted_user: [User]
