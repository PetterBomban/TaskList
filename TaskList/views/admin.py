'''admin stuff'''

from flask import Blueprint, render_template, request, session, redirect, url_for
import user_handler

admin = Blueprint('admin', __name__)

def check_permissions_return_site(user_type, page, error_page='main.login'):
    '''Check to see if the user has the correct permissions
    to view the page'''

    username = session.get('username')
    if not username:
        return redirect(url_for(error_page))
    if not user_handler.check_user_logged_in(username, user_type):
        return redirect(url_for(error_page))

    return render_template(page)

@admin.route('/')
def index():
    '''Main page'''

    return check_permissions_return_site('admin', 'admin.html')


@admin.route('/add_user', methods=['GET', 'POST'])
def add_user():
    '''Takes input from add_user.html and sends to db.'''

    ## If we get a post request, we start adding users
    if request.method == 'POST':
        ## Checks to see if we're a logged in admin account before adding user
        username = session.get('username')
        result = user_handler.check_user_logged_in(username, 'admin')
        if not result:
            return redirect(url_for('main.login'))

        message = None
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']

        db_action = user_handler.create_user(username, email, password, user_type)
        if db_action is True:
            message = 'Successfully created user ' + username
            return render_template('add_user.html', message=message)

    return check_permissions_return_site('admin', 'add_user.html')
