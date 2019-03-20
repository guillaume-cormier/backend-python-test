import pytest
import json

from .utils import add_todo, get_todo_json, login, create_client

@pytest.fixture
def client():
    return create_client()

def test_not_logged_in(client):
    response = add_todo(client, 'description')

    assert 'Location: http://localhost/login' in str(response.headers)
    assert response.status_code == 302

def test_no_description(client):
    login(client)
    response = add_todo(client, '')

    assert response.status_code == 400

def test_success(client):
    login(client)
    add_response = add_todo(client, 'todo added by test')
    get_todo_response = get_todo_json(client, 9)

    todo = json.loads(get_todo_response.data.decode('utf-8'))

    expected_todo = {
        'completed': 0,
        'description': 'todo added by test',
        'id': 9,
        'user_id': 1,
    }

    assert 'Location: http://localhost/todo' in str(add_response.headers)
    assert add_response.status_code == 302
    assert todo == expected_todo
