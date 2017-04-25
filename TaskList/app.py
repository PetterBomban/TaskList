from views import index
from views import admin
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template

APP = Flask(__name__)

## NOTE: Replace this with something else if used in prod.
APP.secret_key = 'devKey_:)'

## Loading blueprints
APP.register_blueprint(index.main)
APP.register_blueprint(admin.admin, url_prefix='/admin')

if __name__ == '__main__':
    APP.run()
