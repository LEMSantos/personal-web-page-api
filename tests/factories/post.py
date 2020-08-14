"""
Factory da model Post
"""


def post_factory(faker):
    return {
        'title': faker.sentence(),
        'image': 'https://source.unsplash.com/random/1600x900',
        'abstract': faker.paragraph(),
        'post_content_id': faker.pyint(),
    }
