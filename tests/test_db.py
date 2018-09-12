import sqlite3
import pytest
from miniURL.db import get_db

def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    
    assert 'closed' in str(e)

def test_init_db(runner, monkeypatch):
    class Recorder(object):
        called = False
    
    def init_db_stub():
        Recorder.called = True
    
    monkeypatch.setattr('miniURL.db.init_db', init_db_stub)
    result = runner.invoke(args=['init-db'])
    assert 'initialized' in result.output
    assert Recorder.called
