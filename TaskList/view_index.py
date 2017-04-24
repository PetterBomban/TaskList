from flask import Blueprint, render_template
import models as db_handler

main = Blueprint('main', __name__)

@main.route('/')
def index():
    '''Main page'''
    return render_template('index.html')

@main.route('/login')
def login():
    '''Handles logins'''
    user = db_handler.login_user('admin', 'APSS')
    return render_template('login.html', user=user)
