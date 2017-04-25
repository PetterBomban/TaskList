from flask import Blueprint, render_template, request
import db_handler

admin = Blueprint('admin', __name__)

@admin.route('/')
def index():
    '''Main page'''
    return render_template('admin.html')

@admin.route('/add_user', methods=['GET', 'POST'])
def add_user():
    '''Takes input from add_user.html and sends to db.'''
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db_handler.create_user(username, email, password)
    return render_template('add_user.html', error=error)
