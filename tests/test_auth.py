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
			"select * from user where username = 'a'",
		).fetchone() is not None