from flaskr import create_app

def test_create_app_is_test_config_aware():
	assert not create_app().testing
	assert create_app({'TESTING': True}).testing

def test_hello(client):
	resp = client.get('/hello')
	assert resp.data == b'Hello, World!'