from flask import Blueprint, render_template, request, session, redirect, url_for
import db_handler

admin = Blueprint('admin', __name__)

@admin.route('/')
def index():
    '''Main page'''
    username = session.get('username')
    if session.get('logged_in') and db_handler.check_user_type(username) == "admin":
        return render_template('admin.html')
    else:
        return redirect(url_for('main.login'))


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
