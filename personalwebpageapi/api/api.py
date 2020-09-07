from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_limiter import Limiter, HEADERS
from flask_limiter.util import get_remote_address
from personalwebpageapi.api.resources import BlogPosts
from personalwebpageapi.api.resources import BlogLatestPosts
from personalwebpageapi.api.resources import BlogPostsWithDrafts

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60 per minute"],
)

limiter.header_mapping = {
    HEADERS.LIMIT: "X-My-Limit",
    HEADERS.RESET: "X-My-Reset",
    HEADERS.REMAINING: "X-My-Remaining"
}

api = Api(app)
CORS(app)

api.add_resource(
    BlogPosts,
    '/posts',
    '/posts/<int:post_id>',
)

api.add_resource(
    BlogLatestPosts,
    '/latest-posts',
)

api.add_resource(
    BlogPostsWithDrafts,
    '/all-posts',
)
