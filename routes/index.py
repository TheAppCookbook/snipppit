from routes.route import Route
import flask


class Index(Route):
    methods = ['GET']
    
    def GET(self, request):
        session = request.values.get("session")
        
        redirect_path = "/story/active"
        if session:
            redirect_path += "?session=" + session
        
        return flask.redirect(redirect_path, code=302)
    