"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
  main.py migrate-task-2-up
  main.py migrate-task-2-down
"""
from docopt import docopt
import subprocess
import os

from alayatodo import app


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
    _run_sql('resources/fixtures.sql')
    _run_sql('resources/migration_task_2_up.sql')

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
