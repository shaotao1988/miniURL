import pytest
from flask import session, g
from miniURL.db import get_db

def test_register(app, client):
    response = client.post('/auth/register', data={
        'username': 'a',
        'password': 'a',
        're_password': 'a'
    })
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        assert get_db().execute("SELECT * from user WHERE username = 'a'"
                            ).fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 're_password', 'message'),(
    ('', '', '', b'Username is required.'),
    ('a', '', '', b'Password is required.'),
    ('a', 'a', '', b'Password is required.'),
    ('a', 'a', 'b', b'Password is not the same.'),
    ('test', 'test', 'test', b'has alread been registered'),
))
def test_register_validate_input(client, username, password, re_password, message):
    response = client.post('/auth/register', data = {
        'username': username,
        'password': password,
        're_password': re_password
    })
    assert message in response.data

def test_login(client, auth):
    response = auth.login()
    assert response.headers['Location'] == "http://localhost/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'),(
    ('', '', b'Username is required'),
    ('test', '', b'Password is required'),
    ('test', 'ttt', b'Incorrect username or password'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
