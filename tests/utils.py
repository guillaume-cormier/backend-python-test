from alayatodo import app
from main import init_db


def create_client():
    app.config['TESTING'] = True
    app.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/alayatodo-test.db'
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()

    with app.app_context():
        init_db()

    return client

def add_todo(client, description):
    return client.post('/todo/', data=dict(
        description=description,
    ))

def get_todos(client, page=1):
    return client.get('/todo/?page=%d' % page)

def get_todo_json(client, todo_id):
    return client.get('/todo/%d/json' % todo_id)

def login(client, username='user1', password='user1'):
    return client.post('/login', data=dict(
        username=username,
        password=password,
    ))
