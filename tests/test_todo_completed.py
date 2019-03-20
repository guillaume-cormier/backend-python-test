import pytest
import json

from .utils import get_todo_json, login, create_client

@pytest.fixture
def client():
    return create_client()

def test_not_logged_in(client):
    response = mark_completed(client, 1, 0)

    assert 'Location: http://localhost/login' in str(response.headers)
    assert response.status_code == 302

def test_toggle_mark_as_completed(client):
    login(client)
    mark_completed_response = mark_completed(client, 1, 1)
    get_todo_json_response_1 = get_todo_json(client, 1)
    mark_not_completed_response = mark_completed(client, 1, 0)
    get_todo_json_response_2 = get_todo_json(client, 1)

    todo_1 = json.loads(get_todo_json_response_1.data.decode('utf-8'))
    todo_2 = json.loads(get_todo_json_response_2.data.decode('utf-8'))

    todo_completed = {
        'completed': 1,
        'description': 'Vivamus tempus',
        'id': 1,
        'user_id': 1,
    }

    todo_not_completed = {
        'completed': 0,
        'description': 'Vivamus tempus',
        'id': 1,
        'user_id': 1,
    }

    assert 'Location: http://localhost/todo' in str(mark_completed_response.headers)
    assert mark_completed_response.status_code == 302
    assert 'Location: http://localhost/todo' in str(mark_not_completed_response.headers)
    assert mark_not_completed_response.status_code == 302
    assert todo_1 == todo_completed
    assert todo_2 == todo_not_completed

def mark_completed(client, id, completed):
    path = '/todo/%d/completed/%d' % (id, completed)
    return client.post(path, follow_redirects=False)
