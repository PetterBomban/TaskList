from flask import Blueprint, render_template, request, session, redirect, url_for
import user_handler
import note_handler

main = Blueprint('main', __name__)

# main page
@main.route('/')
def index():
    if session.get('logged_in') is True:
        username = session.get('username')
        notes = note_handler.get_notes(username)
        return render_template('notes.html', notes=notes)
    else:
        return render_template('notes.html')


# error page
@main.route('/error')
def error():
    error = None
    return render_template('error.html', error=error)


# settings page
@main.route('/settings')
def settings():
    return render_template('settings.html')


# add a new note to the users' note db
@main.route('/newnote', methods=['GET', 'POST'])
def newnote():
    if not session.get('logged_in') or not request.method == 'POST':
        return redirect(url_for('main.index'))

    username = session.get('username')
    title = request.form['title']
    content = request.form['content']
    color = request.form['color']
    if not note_handler.new_note(username, title, content, color):
        return render_template('index.html', message='Failed to create message!')

    return redirect(url_for('main.index'))


# view archived notes
@main.route('/archive', methods=['GET'])
def archive():
    if not session.get('logged_in'):
        return redirect(url_for('main.index'))
    username = session.get('username')
    archived_notes = note_handler.get_notes(username, False, True)
    return render_template('notes.html', notes=archived_notes, archive=True)


# archive a note
@main.route('/archivenote', methods=['GET', 'POST'])
def archivenote():
    if not session.get('logged_in') or not request.method == 'POST':
        return redirect(url_for('main.index'))

    # set the status of the passed note to 2, which means that it's archived
    note_id = request.form['note_id']
    username = session.get('username')
    note_handler.archive_note(username, note_id)
    return redirect(url_for('main.index'))


# permanently delete a note from the archive
@main.route('/deletenote', methods=['GET', 'POST'])
def deletenote():
    if not session.get('logged_in') or not request.method == 'POST':
        return redirect(url_for('main.index'))

    # permanently delete the passed note
    note_id = request.form['note_id']
    username = session.get('username')
    note_handler.permanently_delete_note(username, note_id)
    return redirect(url_for('main.archive'))


# login page
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

    if session.get('logged_in'):
        return redirect(url_for('main.index'))

    return render_template('login.html')


# see ya later aligator 
@main.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('main.index'))
