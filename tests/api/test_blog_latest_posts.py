import pytest
from personalwebpageapi.models.post import Post
from tests.factories import factory
from http import HTTPStatus


@pytest.mark.parametrize('qty_posts', [2, 4])
def test__blog_latest_posts_get(client, qty_posts):
    from operator import itemgetter

    posts = factory(Post, qty_posts).create()

    response = client.get(
        '/latest-posts',
    )

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) <= 3

    sorted_data = sorted(data, key=itemgetter('created_at'), reverse=True)

    assert all(x.items() == y.items() for x, y in zip(data, sorted_data))
