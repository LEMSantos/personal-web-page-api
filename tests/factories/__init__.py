from orator.orm import Factory

from personalwebpageapi.models.post import Post
from personalwebpageapi.models.post_content import PostContent
from personalwebpageapi.models.auth import Auth

from tests.factories.post import post_factory, post_is_draft_factory
from tests.factories.post_content import post_content_factory
from tests.factories.auth import auth_factory

from functools import partial

factory = Factory()

# Post
factory.register(Post, post_factory)
factory.register_as(
    Post,
    'is_draft',
    partial(post_is_draft_factory, factory),
)

# PostContent
factory.register(PostContent, post_content_factory)

# Auth
factory.register(Auth, auth_factory)


__all__ = (
    'factory',
)
