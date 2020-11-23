
import pytest
import materialRecorder

# show print result command : pytest --capture=no

@pytest.fixture
def client():
    with materialRecorder.app.test_client() as client:
        # with materialRecorder.app.app_context():
        #     materialRecorder.init_db()
        yield client

def get_list(client):
    return client.get('record/list').data

def test_record_add(client):
    client.post('/record/add', data=dict(
        name='aa', number=1, record_time=1000, specifications='100m', price='100'
    ))
    client.post('/record/add', data=dict(
        name='bb', number=1, record_time=2000, specifications='10', price='100'
    ))
    client.post('/record/add', data=dict(
        name='cc', number=1, record_time=3000, specifications='20m', price='100'
    ))
    print('-----------------ADD---------------------')
    print(get_list(client))

def test_record_modify(client):
    client.post('/record/modify', data=dict(
        id=1, name='b', number=2, record_time=1000, specifications='100m', price='100'
    ))
    print('-----------------MODIFY---------------------')
    print(get_list(client))

def test_record_delete(client):
    client.delete('/record/delete/2')
    print('-----------------DELETE---------------------')
    print(get_list(client))

def test_record_timeRange(client):
    result = client.post('/record/search/timeRange', data=dict(
        start_time=1000, end_time=1000
    ))
    print('-----------------TIMERANGE---------------------')
    print(result.data)

def test_record_name(client):
    result = client.post('/record/search/name', data=dict(
        name='aa'
    ))
    print('-----------------NAME---------------------')
    print(result.data)

def test_record_specifications(client):
    result = client.post('/record/search/specifications', data=dict(
        specifications='10'
    ))
    print('-----------------SPECIFICATIONS---------------------')
    print(result.data)