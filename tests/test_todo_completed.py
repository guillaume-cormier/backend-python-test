import pytest

from .utils import get_todos, login, create_client

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
    get_todos_response_1 = get_todos(client)
    mark_not_completed_response = mark_completed(client, 1, 0)
    get_todos_response_2 = get_todos(client)

    assert 'Location: http://localhost/todo' in str(mark_completed_response.headers)
    assert mark_completed_response.status_code == 302
    assert 'Location: http://localhost/todo' in str(mark_not_completed_response.headers)
    assert mark_not_completed_response.status_code == 302
    assert b'glyphicon-check' in get_todos_response_1.data
    assert b'glyphicon-check' not in get_todos_response_2.data

def mark_completed(client, id, completed):
    path = '/todo/%d/completed/%d' % (id, completed)
    return client.post(path, follow_redirects=False)
