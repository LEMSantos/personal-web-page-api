from flask_restful import Resource, reqparse
from personalwebpageapi.models.post import Post
from personalwebpageapi.auth import auth
import json


class BlogPostsWithDrafts(Resource):
    def __init__(self):
        self.per_page = 6

    @auth.login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'p',
            type=int,
            dest='page',
            help='Page must be a positive integer',
            required=True,
        )

        args = parser.parse_args()

        posts = Post.paginate(
            self.per_page,
            args.get('page'),
        )

        return {
            'total': posts.total,
            'per_page': posts.per_page,
            'current_page': posts.current_page,
            'last_page': posts.last_page,
            'previous_page': posts.previous_page,
            'next_page': posts.next_page,
            'data': json.loads(posts.to_json()),
        }
