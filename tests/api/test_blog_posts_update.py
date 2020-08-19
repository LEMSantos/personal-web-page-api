import pytest
from personalwebpageapi.models.post import Post
from personalwebpageapi.models.post_content import PostContent
from tests.factories import factory
from http import HTTPStatus


@pytest.mark.parametrize('with_token', [True, False])
def test_blog_posts_update_unauthorized_without_token(client, with_token):
    headers = {
        'Authorization': 'Bearer',
    }

    if with_token:
        headers['Authorization'] = 'Bearer invalid_token'

    response = client.put(
        '/posts/213',
        json={},
        headers=headers,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_blog_posts_update_with_invalid_id(client):
    response = client.put(
        '/posts/21414',
        json={},
        headers={
            'Authorization': 'Bearer valid_token',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_blog_posts_update_without_id(client):
    response = client.put(
        '/posts',
        json={},
        headers={
            'Authorization': 'Bearer valid_token',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_blog_posts_update_unknown_param(client):
    response = client.put(
        '/posts/123',
        json={
            'unknown_param': 'value',
        },
        headers={
            'Authorization': 'Bearer valid_token',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.get_json() == {
        'message': 'Unknown arguments: unknown_param'
    }


def test_blog_posts_update_full_post(client):
    post_content = factory(PostContent).create()
    post = factory(Post).create(post_content_id=post_content.id)

    new_data = factory(Post).make()
    params = {
        'title': new_data.title,
        'image': new_data.image,
        'abstract': new_data.abstract,
        'text': 'test_text',
    }

    response = client.put(
        f'/posts/{post.id}',
        json=params,
        headers={
            'Authorization': 'Bearer valid_token',
        },
    )

    params_copy = params.copy()
    params_copy.pop('text')

    assert response.status_code == HTTPStatus.OK
    assert response.get_json().items() >= params.items()
    assert Post.find(post.id).serialize().items() >= params_copy.items()
    assert PostContent.find(post_content.id).text == params.get('text')


def test_blog_posts_update_partial_post(client):
    post_content = factory(PostContent).create()
    post = factory(Post).create(post_content_id=post_content.id)

    params = {
        'title': 'Novo título',
    }

    response = client.put(
        f'/posts/{post.id}',
        json=params,
        headers={
            'Authorization': 'Bearer valid_token',
        },
    )

    updated_post = Post.find(post.id).serialize()
    updated_post.pop('updated_at')
    updated_title = updated_post.pop('title')

    old_post = post.serialize()
    old_post.pop('updated_at')
    old_title = old_post.pop('title')

    assert updated_title == params['title']
    assert old_post == updated_post
    assert response.get_json()['title'] == params['title']
