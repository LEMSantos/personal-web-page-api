import pytest
from personalwebpageapi.models.post import Post
from personalwebpageapi.models.post_content import PostContent
from tests.factories import factory
from http import HTTPStatus


def test_blog_posts_create_unauthorized_without_token(client):
    response = client.post(
        '/posts',
        json={},
        headers={
            'Authorization': 'Bearer',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_blog_posts_create_unauthorized_invalid_token(client):
    response = client.post(
        '/posts',
        json={},
        headers={
            'Authorization': 'Bearer invalid_token',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize('param_to_remove', ['title', 'image', 'abstract'])
def test_blog_posts_create_without_all_params(client, param_to_remove):
    data = factory(Post).make().serialize()

    data.pop('post_content_id')
    data.pop(param_to_remove, None)
    data.update({
        'text': 'test_text',
    })

    response = client.post(
        '/posts',
        json=data,
        headers={
            'Authorization': 'Bearer valid_token',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert {
        'message': {
            f'{param_to_remove}': ('Missing required parameter in the JSON'
                                   ' body or the post body or the query'
                                   ' string'),
        },
    }


def test_blog_posts_create_Unknown_argument(client):
    data = factory(Post).make().serialize()

    data.pop('post_content_id')
    data.update({
        'text': 'test_text',
        'nonexistent': 'value',
    })

    response = client.post(
        '/posts',
        json=data,
        headers={
            'Authorization': 'Bearer valid_token',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.get_json() == {
        'message': 'Unknown arguments: nonexistent'
    }


def test_blog_posts_create_successfully(client):
    data = factory(Post).make().serialize()

    data.pop('post_content_id')
    data.update({
        'text': 'test_text',
    })

    response = client.post(
        '/posts',
        json=data,
        headers={
            'Authorization': 'Bearer valid_token',
        },
    )

    data = response.get_json()
    saved_post = Post.find(data['id'])
    saved_content = PostContent.find(data['post_content_id'])

    assert response.status_code == HTTPStatus.OK
    assert bool(saved_post)
    assert bool(saved_content)
    assert data.items() >= saved_post.serialize().items()
    assert data['text'] == saved_content.text
