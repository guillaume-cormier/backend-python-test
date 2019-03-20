import pytest

from .utils import add_todo, get_todos, login, create_client

@pytest.fixture
def client():
    return create_client()

def test_not_logged_in(client):
    response = get_todos(client)

    assert 'Location: http://localhost/login' in str(response.headers)
    assert response.status_code == 302

def test_success(client):
    login(client)
    get_todos_response = get_todos(client)

    assert b'Vivamus tempus' in get_todos_response.data
    assert b'Accumsan nunc vitae' in get_todos_response.data
    # owned by user2
    assert b'Lorem ipsum' not in get_todos_response.data

def test_pagination(client):
    login(client)
    initial_todos_response = get_todos(client)
    add_todo(client, 'todo6')
    add_todo(client, 'todo7')
    add_todo(client, 'todo8')
    add_todo(client, 'todo9')
    add_todo(client, 'todo10')
    add_todo(client, 'todo11')
    todos_page_1_response = get_todos(client, 1)
    todos_page_2_response = get_todos(client, 2)
    todos_page_3_response = get_todos(client, 3)

    assert b'Next page' not in initial_todos_response.data
    assert b'Previous page' not in initial_todos_response.data

    assert b'Next page' in todos_page_1_response.data
    assert b'Previous page' not in initial_todos_response.data

    assert b'Next page' in todos_page_2_response.data
    assert b'Previous page' in todos_page_2_response.data

    assert b'Next page' not in todos_page_3_response.data
    assert b'Previous page' in todos_page_3_response.data
