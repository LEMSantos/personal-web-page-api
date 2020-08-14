from flask_restful import Resource
from personalwebpageapi.models.post import Post


class BlogLatestPosts(Resource):
    def __init__(self):
        self.latest_posts_limit = 3

    def get(self):
        posts = Post \
            .all() \
            .sort(lambda item: item.created_at) \
            .reverse() \
            .take(self.latest_posts_limit)

        return posts.serialize()
