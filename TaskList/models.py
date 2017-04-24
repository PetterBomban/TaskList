import sqlite3 as sql
import bcrypt

def create_user(username, password, email):
    '''This function checks the input of the user,
    as well as creating a hashed password'''

    ## Hash the password
    if isinstance(password, str):
        password = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)

    ## Sanitize input
    ## to do
    insert_user(username, hashed_password, email)


def insert_user(username, password, email):
    '''Inserts a user into the users.db
    _note_: Never use this directly. Use create_user()!'''

    con = sql.connect('users.db')
    cur = con.cursor()
    cur.execute('INSERT INTO users (username, password, email) VALUES (?,?,?)', \
        (username, password, email))
    con.commit()
    con.close()
    return True


def login_user(username, password):
    if not check_user_password(password):
        return "Wrong password or username!"






def check_user_password(self, password_to_check):
    '''Checks if the input'ed password matches the DB'''
    if isinstance(password_to_check, str):
        password_to_check = bytes(password_to_check, 'utf-8')
    password = bytes(self.password, 'utf-8')
    return bcrypt.hashpw(password_to_check, password) == password


def get_users():
    '''Gets _ALL_ users'''
    con = sql.connect('users.db')
    cur = con.cursor()
    cur.execute('SELECT username, email FROM users')
    users = cur.fetchall()
    con.close()

    return users



