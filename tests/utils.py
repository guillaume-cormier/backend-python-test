from alayatodo import app
from main import init_db


def create_client():
    app.config['TESTING'] = True
    app.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/alayatodo-test.db'
    client = app.test_client()

    with app.app_context():
        init_db()

    return client

def add_todo(client, description):
    return client.post('/todo/', data=dict(
        description=description,
    ), follow_redirects=False)

def get_todos(client, page=1):
    path = '/todo/?page=%d' % page
    return client.get(path, follow_redirects=False)

def get_todo_json(client, todo_id):
    path = '/todo/%d/json' % todo_id
    return client.get(path, follow_redirects=False)

def login(client, username='user1', password='user1'):
    return client.post('/login', data=dict(
        username=username,
        password=password,
    ), follow_redirects=True)
