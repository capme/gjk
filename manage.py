#!/usr/bin/env python
import os
from flask_script import Manager, Shell
import sys
import subprocess


from app import create_app

is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")

if is_gunicorn:
    # Monkey patch before creating app
    import gevent.monkey
    gevent.monkey.patch_all()

app = create_app()

manager = Manager(app)


@manager.command
def test():
    args = ['flake8', '--ignore=F401', 'app', 'tests']
    p = subprocess.Popen(args)
    p.wait()
    if p.returncode == 0:
        args = ['nosetests', 'tests', '--cover-package', 'app', '--with-coverage']
        p = subprocess.Popen(args)
        p.wait()
    # Exit with return code given from python test
    sys.exit(p.returncode)


def _make_shell_context():
    return dict(app=app,)


manager.add_command('shell', Shell(make_context=_make_shell_context))

if __name__ == '__main__':
    manager.run()
