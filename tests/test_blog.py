import pytest
from flaskr.db import get_db

def test_index_view_contains_session_aware_data(client, auth):
	resp = client.get('/')
	assert b'Log In' in resp.data
	assert b'Register' in resp.data

	auth.login()
	resp = client.get('/')
	assert b'New' in resp.data
	assert b'Log Out' in resp.data
	assert b'test\nbody' in resp.data
	assert b'href="/1/update"' in resp.data


@pytest.mark.parametrize('path',(
	'/create',
	'/1/update',
	'/1/delete',
))
def test_login_required_to_see_restricted_routes(client, path):
	resp = client.post(path)
	assert resp.headers['Location'] == 'http://localhost/auth/login'

def test_author_required_for_restricted_actions(app, client, auth):
	with app.app_context():
		db = get_db()
		db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
		db.commit()
	
	auth.login()
	assert client.post('/1/delete').status_code == 403
	assert client.post('/1/update').status_code == 403
	assert b'/1/update' not in client.get('/').data

@pytest.mark.parametrize('path', (
	'/2/update',
	'/2/delete',
))
def test_server_returns_not_found_when_no_post_exists(client, auth, path):
	auth.login()
	resp = client.post(path)
	assert resp.status_code == 404

def test_create_with_valid_data_succeeds(app, client, auth):
	auth.login()
	assert client.get('/create').status_code == 200

	resp = client.post('/create', data={
		'title': 'created', 
		'body': ''
	})
	assert resp.status_code == 302 # redirect after success

	with app.app_context():
		db = get_db()
		count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
		assert count == 2

def test_update_with_valid_data_succeeds(app, client, auth):
	auth.login()
	assert client.get('/1/update').status_code == 200

	resp = client.post('/1/update', data={
		'title': 'updated', 
		'body': ''
	})
	assert resp.status_code == 302 # redirect after success

	with app.app_context():
		db = get_db()
		post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
		assert post['title'] == 'updated'


@pytest.mark.parametrize('path', (
	'/create',
	'/1/update',
))
def test_validation_prevents_invalid_creates_and_updates(client, auth, path):
	auth.login()

	resp = client.post(path, data={
		'title': '', 
		'body': ''
	})

	assert  b'Title is required' in resp.data