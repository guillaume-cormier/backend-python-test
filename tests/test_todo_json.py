import pytest
import json

from .utils import get_todo_json, login, create_client

@pytest.fixture
def client():
    return create_client()

def test_not_logged_in(client):
    response = get_todo_json(client, 1)

    assert 'Location: http://localhost/login' in str(response.headers)
    assert response.status_code == 302

def test_wrong_user(client):
    login(client, username='user2', password='user2')
    # id 1 belongs to user1
    response = get_todo_json(client, 1)

    assert response.status_code == 404

def test_success(client):
    login(client)
    response = get_todo_json(client, 1)

    expected_todo = {
        'completed': 0,
        'description': 'Vivamus tempus',
        'id': 1,
        'user_id': 1,
    }
    todo = json.loads(response.data.decode('utf-8'))

    assert expected_todo == todo
    assert response.status_code == 200
