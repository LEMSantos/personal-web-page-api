from personalwebpageapi.models.post import Post
from personalwebpageapi.models.post_content import PostContent
from tests.factories import factory
from http import HTTPStatus


def test_blog_posts_with_drafts_get_without_token(client):
    headers = {
        'Authorization': 'Bearer',
    }

    response = client.get(
        '/all-posts',
        query_string='p=1',
        headers=headers,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_blog_posts_with_drafts_get_invalid_token(client):
    headers = {
        'Authorization': 'Bearer invalid_token',
    }

    response = client.get(
        '/all-posts',
        query_string='p=1',
        headers=headers,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_paginated_posts_without_page_param(client):
    response = client.get(
        '/all-posts',
        headers={
            'Authorization': 'Bearer valid_token',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.get_json() == {
        'message': {
            'p': 'Page must be a positive integer',
        },
    }


def test_get_paginated_posts_empty_database(client):
    response = client.get(
        '/all-posts',
        query_string='p=1',
        headers={
            'Authorization': 'Bearer valid_token',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {
        'total': 0,
        'per_page': 6,
        'current_page': 1,
        'last_page': 0,
        'previous_page': None,
        'next_page': None,
        'data': [],
    }


def test_get_paginated_posts_successfully(client):
    posts = factory(Post, 7).create()
    factory(Post, 'is_draft', 2).create()

    response = client.get(
        '/all-posts',
        query_string='p=1',
        headers={
            'Authorization': 'Bearer valid_token',
        },
    )

    data = response.get_json()
    expected_data = posts.serialize()

    assert response.status_code == HTTPStatus.OK
    assert data.items() >= {
        'total': 9,
        'per_page': 6,
        'current_page': 1,
        'last_page': 2,
        'previous_page': None,
        'next_page': 2,
    }.items()
    assert isinstance(data['data'], list) and len(data['data']) == 6
    assert all(item in expected_data for item in data['data'])
