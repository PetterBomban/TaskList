import sqlite3 as sql
import bcrypt

def login_user(username, password):
    '''Used for logging in the user'''
    return check_user_details(username, password)

def check_user_details(username, password_to_check):
    '''Used for checking user details before login'''
    con = sql.connect('users.db')
    cur = con.cursor()
    cur.execute('SELECT username, password FROM users WHERE username = ?', (username,))
    user = cur.fetchall()
    con.close()

    ## if user (list) is empty, it means that the username did not match anything in the db
    password_to_check_enc = bytes(password_to_check, 'utf-8')
    password_from_db = bytes(user[0][1], 'utf-8')
    if not user:
        return False
    elif not bcrypt.checkpw(password_to_check_enc, password_from_db):
        return False
    else:
        return True


def check_user_type(username):
    '''Checks the user type against the database'''
    con = sql.connect('users.db')
    cur = con.cursor()
    cur.execute('SELECT user_type FROM users WHERE username = ?', (username,))
    user_type = cur.fetchall()
    con.close()

    return user_type[0][0]


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
