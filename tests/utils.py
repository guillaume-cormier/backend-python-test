def add_todo(client, description):
    return client.post('/todo/', data=dict(
        description=description,
    ), follow_redirects=False)

def get_todos(client):
    return client.get('/todo/', follow_redirects=False)

def login(client, username='user1', password='user1'):
    return client.post('/login', data=dict(
        username=username,
        password=password,
    ), follow_redirects=True)
