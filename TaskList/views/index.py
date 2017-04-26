'''index stuff'''

from flask import Blueprint, render_template, request, session, redirect, url_for
import user_handler

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if session.get('logged_in') is True:
        username = session.get('username')
        return render_template('index.html', username=username)
    else:
        return render_template('index.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    error_message = 'Incorrect username or password.'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        login_user = user_handler.login_user(username, password)
        if login_user is True:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('main.index'))
        else:
            return render_template('login.html', error=error_message)

    return render_template('login.html')


@main.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('main.index'))
