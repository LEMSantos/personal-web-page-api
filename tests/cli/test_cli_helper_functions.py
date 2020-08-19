from personalwebpageapi.cli import token_generator


def test_token_generator():
    token = token_generator(size=50)

    assert isinstance(token, str)
    assert len(token) == 50
