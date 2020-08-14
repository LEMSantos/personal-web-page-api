import env
import click
import waitress
from paste.translogger import TransLogger
from logging.config import fileConfig
from personalwebpageapi.api import app
from personalwebpageapi.models.auth import Auth

fileConfig('config/logging.conf')


def token_generator(size=6):
    import string
    import random

    chars = ''.join([
        string.ascii_uppercase,
        string.digits,
        string.ascii_lowercase,
    ])

    return ''.join(random.choice(chars) for _ in range(size))


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        if env.APP_ENV == 'prod':
            waitress.serve(
                TransLogger(app, setup_console_handler=False),
                host=env.WAITRESS_HOST,
                port=env.WAITRESS_PORT,
                threads=env.WAITRESS_JOBS,
            )
        else:
            app.run(
                host='0.0.0.0',
                port='5000',
                debug=True
            )


@cli.command('token')
@click.option('-c', '--create', is_flag=True)
@click.option('-l', '--list', '_list', is_flag=True)
def token(create, _list):
    if _list:
        for authorization in Auth.all():
            print(authorization.token)

        return None

    if create:
        _token = token_generator(100)

        while Auth.where('token', '=', _token).first():
            _token = token_generator(100)

        authorization = Auth()
        authorization.token = _token
        authorization.save()

        print(_token)

        return None

    raise click.BadArgumentUsage('no option provided')
