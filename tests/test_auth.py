import pytest
from flask import g, session
from flaskr.db import get_db

def test_register_with_valid_user_creates_new_user(client, app):
	assert client.get('/auth/register').status_code == 200

	resp = client.post(
		'/auth/register',
		data = {'username': 'a', 'password': 'a'}	
	)
	assert 'http://localhost/auth/login' == resp.headers['Location']

	with app.app_context():
		assert get_db().execute(
			"select username from user where username = 'a'",
		).fetchone()['username']== 'a'

@pytest.mark.parametrize(('username', 'password', 'message'),(
		('', '', b'Username is required.'),
		('a', '', b'Password is required.'),
		('test', 'test', b'already registered'),
))
def test_register_fails_when_provided_with_invalid_data(client, username, password, message):
	resp = client.post(
		'/auth/register',
		data = {'username': username, 'password': password}
	)

	assert message in resp.data

def test_login_creates_expected_session_data(client, auth):
	assert client.get('/auth/login').status_code == 200
	resp = auth.login()
	assert resp.headers['Location'] == 'http://localhost/'

	with client:
		client.get('/')
		assert session['user_id'] == 1
		assert g.user['username'] == 'test'

def test_logout_clears_session(client, auth):
	auth.login()

	with client:
		auth.logout()
		assert 'user_id' not in session
