from routes.route import Route

from parse_rest.user import User
from parse_rest.connection import SessionToken
from parse_rest.core import ResourceRequestBadRequest

import flask


class Index(Route):
    methods = ['GET']
    
    def GET(self, request):
        return flask.redirect("/story/active", code=302)
        
class Login(Route):
    methods = ['GET', 'POST']
    
    def GET(self, request):
        return "LOGIN PAGE"
        
    def POST(self, request):
        username = request.values.get("username")
        password = request.values.get("pw_hash")
        
        try:
            user = User.signup(
                username,
                password
            )
        except ResourceRequestBadRequest:
            user = User.login(
                username,
                password
            )

        return user.sessionToken
