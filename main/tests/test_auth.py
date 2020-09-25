from flask import g, session
import pytest

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email='test@example.com', password='test'):
        return self._client.post(
            '/login',
            data={'email': email, 'password': password}
        )

    def logout(self):
        return self._client.get('/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)

def test_register(client, app):
    assert client.get('/register').status_code == 200
    response = client.post(
        '/register', data={'email': 'a@test.com', 'password': 'a'}
    )
    assert 'http://localhost/login' == response.headers['Location']

    with app.app_context():
        assert User.query.filter_by(email='a@test.com').first() is not None


@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('', '', b'Email is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, email, password, message):
    response = client.post(
        '/register',
        data={'email': email, 'password': password}
    )
    assert message in response.data

def test_login(client, auth):
    assert client.get('/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['email'] == 'test@example.com'


@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('a', 'test', b'Invalid username/password combination'),
    ('test@example.com', 'a', b'Invalid username/password combination'),
))
def test_login_validate_input(auth, email, password, message):
    response = auth.login(email, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
