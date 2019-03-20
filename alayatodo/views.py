from alayatodo import app
from flask import (
    abort,
    flash,
    g,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session
    )


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = f.read()
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    return render_template('todo.html', todo=todo)

@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    if not session.get('logged_in'):
        return redirect('/login')

    cur = g.db.execute(
        "SELECT * FROM todos WHERE id = %d and user_id = %d" \
        % (int(id), int(session['user']['id']))
    )
    todo = cur.fetchone()

    if not todo:
        abort(404)

    return jsonify(dict(todo))

@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    cur = g.db.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    description = request.form.get('description')

    if not description:
        return make_response("Description is required", 400)

    g.db.execute(
        "INSERT INTO todos (user_id, description) VALUES ('%s', '%s')"
        % (session['user']['id'], description)
    )
    g.db.commit()

    flash('Item created.')

    return redirect('/todo')


@app.route('/todo/<id>/completed/<completed>', methods=['POST'])
def todo_completed(id, completed):
    if not session.get('logged_in'):
        return redirect('/login')

    g.db.execute(
        "UPDATE todos SET completed = %d WHERE user_id = %d and id = %d"
        % (int(completed), int(session['user']['id']), int(id))
    )
    g.db.commit()
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')

    cursor = g.db.cursor()
    cursor.execute(
        "DELETE FROM todos WHERE user_id = %d and id = %d"
        % (session['user']['id'], int(id))
    )
    g.db.commit()
    if cursor.rowcount == 0:
        abort(404)

    flash('Item deleted.')

    return redirect('/todo')
