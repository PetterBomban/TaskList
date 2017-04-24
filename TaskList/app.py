''' How the app will work
    users.db
        This will handle registration, authentication etc.
        Contains no tasks, only a refrence to the name of the
        specific users' task db.

    tasks_USERNAME.db
        One database per user. Contains the users' individual
        tasks
https://gist.github.com/PolBaladas/07bfcdefb5c1c57cdeb5
'''

from view_index import main
from view_admin import admin
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template

APP = Flask(__name__)

## Loading blueprints
APP.register_blueprint(main)
APP.register_blueprint(admin, url_prefix='/admin')

if __name__ == '__main__':
    APP.run()

'''routing with variable in url
@APP.route('/<var>')
def route(var="default value"):
    return render_template('page.html', var=var)
'''