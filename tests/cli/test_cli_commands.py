import mock
import pytest
import env
from click.testing import CliRunner
from personalwebpageapi.cli import cli


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
