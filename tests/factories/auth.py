"""
Factory da model Auth
"""


def auth_factory(faker):
    return {
        'token': faker.pystr(100, 100),
    }
