
import pytest
import materialRecorder

@pytest.fixture
def client():
    with materialRecorder.app.test_client() as client:
        # with materialRecorder.app.app_context():
        #     materialRecorder.init_db()
        yield client

def test_record_add(client):
    client.post('/record/add', data=dict(
        name='a', number=1, record_time=1000, specifications='100m', price='100'
    ))