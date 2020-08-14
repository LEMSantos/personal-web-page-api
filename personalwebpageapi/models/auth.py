"""Definicao do model Auth"""
from personalwebpageapi.models import Model
from orator import SoftDeletes


class Auth(SoftDeletes, Model):
    """Model Auth"""

    __table__ = 'auth'
    __dates__ = [
        'created_at',
        'deleted_at',
        'updated_at',
    ]
