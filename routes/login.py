from parse_rest.user import User
from parse_rest.connection import SessionToken
from parse_rest.core import ResourceRequestBadRequest

from routes.route import Route
import flask


class Login(Route):
    methods = ['GET', 'POST']
    
    def GET(self, request):
        return flask.render_template("signup.html")
        
    def POST(self, request):
        username = request.values.get("email").lower()
        password = request.values.get("password")
        
        try:
            user = User.signup(
                username,
                password,
                email=username,
                first_name=request.values.get("first_name"),
                last_name=request.values.get("last_name")
            )
        except ResourceRequestBadRequest:
            user = User.login(
                username,
                password
            )

        response = flask.make_response(
            flask.redirect("/")
        )

        response.set_cookie("session", user.sessionToken)
        return response

class Logout(Route):
    methods = ['GET']
    
    def GET(self, request):
        response = flask.make_response(
            flask.redirect("/")
        )

        response.set_cookie("session", "", expires=0)
        return response

class PasswordReset(Route):
    methods = ['GET']
    
    def GET(self, request):
        email = request.values.get("email").lower()
        User.request_password_reset(
            email=email
        )
        
        return flask.redirect('/')