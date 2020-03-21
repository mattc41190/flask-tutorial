import sqlite3 
import pytest
from flaskr.db import get_db

def test_get_db_always_returns_same_db_instance(app):
	with app.app_context():
		db = get_db()
		assert db == get_db()
	
	with pytest.raises(sqlite3.ProgrammingError) as e:
		db.execute('SELECT 1')
	
	assert 'closed' in str(e.value)

def test_init_db_cli_command_calls_init_db_func(runner, monkeypatch):
	class Recorder(object):
		called = False
	
	def fake_init_db():
		Recorder.called = True

	monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
	result = runner.invoke(args=['init-db']) # cli command
	assert 'Initialized' in result.output
	assert Recorder.called