"""Definicao do model PostContent"""
from personalwebpageapi.models import Model
from orator import SoftDeletes


class PostContent(SoftDeletes, Model):
    """Model PostContent"""

    __table__ = 'post_contents'
