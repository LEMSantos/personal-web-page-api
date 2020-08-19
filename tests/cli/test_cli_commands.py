import mock
import pytest
import env
import click
from click.testing import CliRunner
from tests.factories import factory
from personalwebpageapi.cli import cli
from personalwebpageapi.models.auth import Auth


@pytest.fixture
def runner():
    return CliRunner()


@mock.patch('flask.Flask.run')
def test_cli_dev_command_without_command(mocker, runner):
    mocker.return_value = None

    env.APP_ENV = 'dev'
    result = runner.invoke(cli)

    assert result.exit_code == 0
    mocker.assert_called_once()


@mock.patch('waitress.serve')
def test_cli_prod_command_without_command(mocker, runner):
    mocker.return_value = None

    env.APP_ENV = 'prod'
    result = runner.invoke(cli)

    assert result.exit_code == 0
    mocker.assert_called_once()


def test_cli_token_command_without_params(runner):
    result = runner.invoke(cli, ['token'])
    assert 'Error: no option provided' in result.output


def test_cli_token_list(runner):
    factory(Auth).create(token='token_1')
    factory(Auth).create(token='token_2')

    result = runner.invoke(cli, ['token', '-l'])

    assert result.exit_code == 0
    assert result.output == 'token_1\ntoken_2\n'


@mock.patch('personalwebpageapi.cli.token_generator')
def test_cli_token_create(mocker, runner):
    mocker.return_value = 'test_token'

    result = runner.invoke(cli, ['token', '-c'])
    auth_token = Auth.where('token', 'test_token').get()

    assert auth_token
    mocker.assert_called_with(100)
