"""Definicao do model Post"""
from personalwebpageapi.models import Model
from personalwebpageapi.models.post_content import PostContent
from orator import SoftDeletes
from orator.orm import has_one


class Post(SoftDeletes, Model):
    """Model Post"""

    __table__ = 'posts'
    __dates__ = [
        'created_at',
        'deleted_at',
        'updated_at',
    ]
    __hidden__ = ['deleted_at']

    @has_one('id', 'post_content_id')
    def post_content(self):
        return PostContent
