from alayatodo import app, db
from alayatodo.models import Todos, Users
from flask import (
    abort,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


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

    user = Users.query.filter_by(username=username).first()
    if not user:
        return redirect('/login')

    if not user.is_valid_password(password):
        return redirect('/login')

    if not id:
        return redirect('/login')

    session['user'] = user.to_dict()
    session['logged_in'] = True
    return redirect('/todo')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
@login_required
def todo(id):
    todo = Todos.query.filter_by(user_id=session['user']['id'], id=id).first()

    if not todo:
        abort(404)

    return render_template('todo.html', todo=todo)

@app.route('/todo/<id>/json', methods=['GET'])
@login_required
def todo_json(id):
    todo = Todos.query.filter_by(user_id=session['user']['id'], id=id).first()

    if not todo:
        abort(404)

    return jsonify(todo.to_dict())

@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
@login_required
def todos():
    page = request.args.get('page', 1, type=int)
    todos = Todos.query.filter_by(user_id=session['user']['id']).paginate(page, 5, False)

    next_url = url_for('todos', page=todos.next_num) if todos.has_next else None
    prev_url = url_for('todos', page=todos.prev_num) if todos.has_prev else None

    return render_template('todos.html', todos=todos.items, next_url=next_url, prev_url=prev_url)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
@login_required
def todos_POST():
    description = request.form.get('description')

    if not description:
        return make_response("Description is required", 400)

    db.session.add(Todos(user_id=session['user']['id'], description=description))
    db.session.commit()

    flash('Item created.')

    return redirect('/todo')


@app.route('/todo/<id>/completed/<completed>', methods=['POST'])
@login_required
def todo_completed(id, completed):
    updated = db.session.query(Todos)\
        .filter_by(
            user_id=session['user']['id'],
            id=id
        ).update({"completed": True if completed == '1' else False})
    db.session.commit()

    if not updated:
        return abort(404)

    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
@login_required
def todo_delete(id):
    deleted = db.session.query(Todos)\
        .filter_by(
            user_id=session['user']['id'],
            id=id
        ).delete()
    db.session.commit()

    if not deleted:
        abort(404)

    flash('Item deleted.')

    return redirect('/todo')
