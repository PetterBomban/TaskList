from flask import Blueprint, render_template, request, session, redirect, url_for
import user_handler
import note_handler

admin = Blueprint('admin', __name__)

# check to see if the user has the correct permissions to view the page
def check_permissions_return_site(user_type, page, error_page='main.login'):
    username = session.get('username')
    if not username:
        return redirect(url_for(error_page))
    if not user_handler.check_user_logged_in(username, user_type):
        return redirect(url_for(error_page))
    return render_template(page)


# main page
@admin.route('/')
def index():
    return check_permissions_return_site('admin', 'admin.html')


# add a new user to the users db
@admin.route('/add_user', methods=['GET', 'POST'])
def add_user():
    # if we get a post request, we start adding users
    if request.method == 'POST':
        # checks to see if we're a logged in admin account before adding user
        username = session.get('username')
        result = user_handler.check_user_logged_in(username, 'admin')
        if not result:
            return redirect(url_for('main.login'))

        # create the user in the users db
        message = None
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        db_action = user_handler.create_user(username, email, password, user_type)
        if not db_action:
            message = 'Could not create user ' + username + '!'
            render_template('add_user.html', message=message)
        
        # create username_notes.db and table
        note_db_action = note_handler.create_note_db_table(username)
        if not note_db_action:
            message = 'Could not create user note db ' + username + '!'
            render_template('add_user.html', message=message)
        
        # return with success message
        message = 'Successfully created user ' + username + '.'
        return render_template('add_user.html', message=message)

    # check for admin rights
    return check_permissions_return_site('admin', 'add_user.html')
