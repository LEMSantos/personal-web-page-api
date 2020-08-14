import os
import env
import pytest
import importlib
from tests.factories import factory
from orator.migrations import Migrator, DatabaseMigrationRepository


def pytest_configure(config):
    env_testing = importlib.__import__('env_testing')
    variables_env_testing = set(
        filter(lambda x: not x.startswith('__'), dir(env_testing))
    )

    for key in variables_env_testing:
        setattr(env, key, getattr(env_testing, key))


def pytest_runtest_setup():
    from personalwebpageapi.models import db

    migrations_path = f'{os.getcwd()}/migrations'

    repository = DatabaseMigrationRepository(
        db,
        'migrations',
    )
    migrator = Migrator(repository, db)

    if not migrator.repository_exists():
        repository.create_repository()

    migrator.set_connection(db.get_default_connection())
    migrator.run(migrations_path)


def pytest_runtest_teardown():
    from personalwebpageapi.models import db

    migrations_path = f'{os.getcwd()}/migrations'

    repository = DatabaseMigrationRepository(
        db,
        'migrations',
    )
    migrator = Migrator(repository, db)

    if not migrator.repository_exists():
        repository.create_repository()

    migrator.set_connection(db.get_default_connection())
    migrator.reset(migrations_path)


@pytest.fixture
def client():
    from personalwebpageapi.api import app
    from personalwebpageapi.models.auth import Auth

    factory(Auth).create(token='valid_token')

    app.config['TESTING'] = True
    test_client = app.test_client()

    return test_client
