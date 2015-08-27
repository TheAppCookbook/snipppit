import os
from flask import Flask, request

from commons import parse_client

from routes.index import Index
from routes.login import Login, PasswordReset
from routes.story import Story, Stories
from routes.post import Post, Vote


app = Flask(__name__)

# Routes
@app.route('/', methods=Index.methods)
def _index():
    return Index().route(request)
    
# ... login
@app.route('/login', methods=Login.methods)
def _login():
    return Login().route(request)
    
@app.route('/forgot', methods=PasswordReset.methods)
def _forgot():
    return PasswordReset().route(request)
    
# ... stories
@app.route('/story', methods=Story.methods)
@app.route('/story/<story_id>', methods=Story.methods)
def _story(story_id='active'):
    return Story().route(request, story_id)

@app.route('/stories', methods=Stories.methods)
def _stories():
    return Stories().route(request)
    
# ... posts & votes
@app.route('/post', methods=Post.methods)
def _post():
    return Post().route(request)
    
@app.route('/post/<post_id>/vote', methods=Vote.methods)
def _vote(post_id):
    return Vote().route(request, post_id)

app.debug = True
if __name__ == "__main__":
    app.run()