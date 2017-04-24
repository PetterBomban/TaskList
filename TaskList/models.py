import sqlite3 as sql
import bcrypt

def login_user(username, password):
    '''Used for logging in the user'''
    user_details = check_user_details(username, password)
    return user_details

def check_user_details(username, password_to_check):
    '''Used for checking user details before login'''
    error_message = 'Username or password is incorrect.'

    con = sql.connect('users.db')
    cur = con.cursor()
    cur.execute('SELECT username, password FROM users WHERE username = ?', (username,))
    user = cur.fetchall()
    con.close()

    ## if user (list) is empty, it means that the username did not match anything in the db
    password_to_check_enc = bytes(password_to_check, 'utf-8')
    password_from_db = bytes(user[0][1], 'utf-8')
    if not user:
        return error_message
    elif not bcrypt.checkpw(password_to_check_enc, password_from_db):
        return error_message
    else:
        return "Logged in!" + str(user[0][0])


def create_user(username, email, password):
    '''Used for creating users'''
    ## Hash the password
    password = bytes(password, 'utf-8')
    password_hashed = str(bcrypt.hashpw(password, bcrypt.gensalt()), 'utf8')
    ## Sanitize input
    ## to do
    insert_user(username, email, password_hashed)


def insert_user(username, email, password):
    '''DO NOT USE. Use create_user()'''
    con = sql.connect('users.db')
    cur = con.cursor()
    cur.execute('INSERT INTO users (username, email, password) VALUES (?,?,?)', \
        (username, email, password))
    con.commit()
    con.close()
    return True
