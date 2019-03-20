"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
  main.py migrate-task-2-up
  main.py migrate-task-2-down
"""
from alayatodo import app, db
from alayatodo.models import Todos, Users
from docopt import docopt
from passlib.hash import bcrypt
import os
import subprocess


def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError as ex:
        print(ex.output)
        os._exit(1)


def init_db():
    _run_sql('resources/database.sql')
    _run_sql('resources/migration_task_2_up.sql')
    _add_db_fixtures()

def _add_db_fixtures():
    db.session.add(Users(username='user1', password=bcrypt.hash('user1')))
    db.session.add(Users(username='user2', password=bcrypt.hash('user2')))
    db.session.add(Users(username='user3', password=bcrypt.hash('user3')))

    db.session.add(Todos(user_id=1, description='Vivamus tempus'))
    db.session.add(Todos(user_id=1, description='lorem ac odio'))
    db.session.add(Todos(user_id=1, description='Ut congue odio'))
    db.session.add(Todos(user_id=1, description='Sodales finibus'))
    db.session.add(Todos(user_id=1, description='Accumsan nunc vitae'))
    db.session.add(Todos(user_id=2, description='Lorem ipsum'))
    db.session.add(Todos(user_id=2, description='In lacinia est'))
    db.session.add(Todos(user_id=2, description='Odio varius gravida'))

    db.session.commit()

if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        init_db()
        print("AlayaTodo: Database initialized.")
    elif args['migrate-task-2-up']:
        _run_sql('resources/migration_task_2_up.sql')
        print("AlayaTodo: Task 2 migration complete.")
    elif args['migrate-task-2-down']:
        _run_sql('resources/migration_task_2_down.sql')
        print("AlayaTodo: Task 2 migration reverted.")
    else:
        app.run(use_reloader=True)
