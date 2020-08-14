"""
Factory da model PostContent
"""


def post_content_factory(faker):
    return {
        'text': faker.text(1000),
    }
