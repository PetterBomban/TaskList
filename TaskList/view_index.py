from flask import Blueprint, render_template
main = Blueprint('main', __name__)

@main.route('/')
def index():
    '''Main page'''
    return render_template('index.html')

@main.route('/login')
def login():
    '''Handles logins'''
    return render_template('login.html')
