import sqlite3
from materialRecorder.utils import RecordSql
import pytest

@pytest.fixture()
def cursor():
    db = sqlite3.connect(
            'materialRecorder.sqlite',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
    with open('schema.sql') as f:
        db.executescript(f.read())
    cursor = db.cursor()
    return cursor

def test_modify_no_exist_record(cursor):
    json_data = dict(
        id=1000, name='aa', number=1, record_time=1000, specifications='100m', price='100'
    )
    cursor.execute(RecordSql.modify_record(json_data))
    print('------------------MODIFY_NO_EXIST----------------')
    print(cursor.fetchall())

def test_delete_no_exist_record(cursor):
    cursor.execute(RecordSql.delete_record(1022))
    print('------------------DELETE_NO_EXIST----------------')
    print(cursor.fetchall())

