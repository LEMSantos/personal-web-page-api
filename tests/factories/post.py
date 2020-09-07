"""
Factory da model Post
"""
from personalwebpageapi.models.post import Post


def post_factory(faker):
    return {
        'title': faker.sentence(),
        'image': 'https://source.unsplash.com/random/1600x900',
        'abstract': faker.paragraph(),
        'post_content_id': faker.pyint(),
        'is_draft': False,
    }


def post_is_draft_factory(factory, faker):
    post = factory.raw(Post)

    post.update({
        'is_draft': True,
    })

    return post
