from views import index
from views import admin
from flask import Flask, request, session, redirect, url_for, abort, \
    render_template

APP = Flask(__name__)

## NOTE: Replace this with something else if used in prod.
APP.secret_key = 'devKey_:)'

## Loading blueprints
APP.register_blueprint(index.main)
APP.register_blueprint(admin.admin, url_prefix='/admin')

@APP.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    APP.run()
