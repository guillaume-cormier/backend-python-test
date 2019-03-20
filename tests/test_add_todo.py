import pytest

from .utils import add_todo, get_todos, login, create_client

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
    get_todos_response = get_todos(client)

    assert 'Location: http://localhost/todo' in str(add_response.headers)
    assert add_response.status_code == 302
    assert b'todo added by test' in get_todos_response.data
