from flask import g, session
from main.models import User
import pytest


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email='test@example.com', password='test456'):
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
        '/register', data=dict(email='a@example.com', password='test123'))
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        assert User.query.filter_by(email='a@example.com').first() is not None


def test_register_validate_input(client, message=b'Select a stronger password.'):
    response = client.post(
        '/register', data=dict(email='a@example.com', password='123'), follow_redirects=True)
    assert message in response.data


def test_login(client, test_user):
    assert client.get('/login').status_code == 200
    response = client.post(
        '/login', data=dict(email='test@example.com', password='test456'), follow_redirects=True)
    assert bytes('/user/{}'.format(test_user.id).encode()) in response.data
    assert b'Your unlearning journey' in response.data


def test_login_validate_input(client, message=b'Invalid email/password combination'):
    response = client.post(
        '/login', data=dict(email='test@example.com', password='test1234'), follow_redirects=True)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
