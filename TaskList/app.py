''' How the app will work
    users.db
        This will handle registration, authentication etc.
        Contains no tasks, only a refrence to the name of the
        specific users' task db.

    tasks_USERNAME.db
        One database per user. Contains the users' individual
        tasks
'''

import sqlite3 as sql
from view_index import main
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template

APP = Flask(__name__)

## Loading blueprints
APP.register_blueprint(main)

if __name__ == '__main__':
    APP.run()

'''routing with variable in url
@APP.route('/<var>')
def route(var="default value"):
    return render_template('page.html', var=var)
'''