from flask_httpauth import HTTPTokenAuth
from personalwebpageapi.models.auth import Auth

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    token = Auth.where('token', '=', token).first()

    if token:
        return True

    return False
