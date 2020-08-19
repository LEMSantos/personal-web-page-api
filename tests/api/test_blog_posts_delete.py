import pytest
from personalwebpageapi.models.post import Post
from personalwebpageapi.models.post_content import PostContent
from tests.factories import factory
from http import HTTPStatus


@pytest.mark.parametrize('with_token', [True, False])
def test_blog_posts_delete_unauthorized(client, with_token):
    headers = {
        'Authorization': 'Bearer',
    }

    if with_token:
        headers['Authorization'] = 'Bearer invalid_token'

    response = client.delete(
        '/posts/123',
        headers=headers,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED



def test_blog_posts_delete_with_invalid_id(client):
    response = client.delete(
        '/posts/1234',
        headers={
            'Authorization': 'Bearer valid_token',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_blog_posts_delete_without_id(client):
    response = client.delete(
        '/posts',
        headers={
            'Authorization': 'Bearer valid_token',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_blog_posts_delete_successfully(client):
    post_content = factory(PostContent).create()
    post = factory(Post).create(post_content_id=post_content.id)

    response = client.delete(
        f'/posts/{post.id}',
        headers={
            'Authorization': 'Bearer valid_token',
        },
    )

    data = response.get_json()

    assert 'message' in data
    assert data.get('message') == 'Successfully deleted'
    assert not Post.find(post.id)
    assert not PostContent.find(post_content.id)
