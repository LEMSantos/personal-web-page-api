from flask_restful import Resource, reqparse, abort
from personalwebpageapi.models.post import Post
from personalwebpageapi.models.post_content import PostContent
from personalwebpageapi.auth import auth
from http import HTTPStatus
import json


class BlogPosts(Resource):
    def __init__(self):
        self.per_page = 6

    def get(self, post_id=None):
        if post_id:
            post = Post.find(post_id)

            if not post:
                abort(HTTPStatus.NOT_FOUND)

            response = post.serialize()
            response.update({
                'text': post.post_content.text,
            })

            return response
        else:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'p',
                type=int,
                dest='page',
                help='Page must be a positive integer',
                required=True,
            )

            args = parser.parse_args()

            posts = (Post
                .where('is_draft', False)
                .paginate(
                    self.per_page,
                    args.get('page'),
                )
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

    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('title', required=True)
        parser.add_argument('image', required=True)
        parser.add_argument('abstract', required=True)
        parser.add_argument('text', required=True)
        parser.add_argument('is_draft', type=bool)

        args = parser.parse_args(strict=True)

        post_content = PostContent()
        post_content.text = args.get('text')
        post_content.save()

        post = Post()
        post.title = args.get('title')
        post.image = args.get('image')
        post.abstract = args.get('abstract')
        post.post_content_id = post_content.id
        post.is_draft = False
        post.save()

        return {
            **post.serialize(),
            'text': post_content.text,
        }

    @auth.login_required
    def put(self, post_id=None):
        parser = reqparse.RequestParser()

        parser.add_argument('title', store_missing=False)
        parser.add_argument('image', store_missing=False)
        parser.add_argument('abstract', store_missing=False)
        parser.add_argument('text', store_missing=False)
        parser.add_argument('is_draft', type=bool, store_missing=False)

        args = parser.parse_args(strict=True)

        post = Post.find(post_id)

        if not post:
            abort(HTTPStatus.NOT_FOUND)

        post_content = PostContent.find(post.post_content_id)

        if 'text' in args:
            post_content.text = args.get('text')
            post_content.save()

            args.pop('text', None)

        for key in args:
            setattr(post, key, args.get(key))

        post.save()

        return {
            **post.serialize(),
            'text': post_content.text,
        }

    @auth.login_required
    def delete(self, post_id=None):
        post = Post.find(post_id)

        if not post:
            abort(HTTPStatus.NOT_FOUND)

        post_content = PostContent.find(post.post_content_id)

        if post_content:
            post_content.delete()

        post.delete()

        return {
            'message': 'Successfully deleted',
        }
