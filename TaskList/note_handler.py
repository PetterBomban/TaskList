import sqlite3 as sql
import user_handler
import os
from flask import session

DB_STATUS = {'available': 1, 'archived': 2}


def get_notes(username):
    db = get_note_db(username)
    sql = 'SELECT title,content,color,note_id FROM notes ORDER BY note_id desc'
    db['cur'].execute(sql)
    notes = db['cur'].fetchall()
    db['con'].close()
    return notes


# creates a note database for the current user like so: username_tasks.db
def new_note(username, title, content, color, status=DB_STATUS['available']):
    # check for users' note database
    db = get_note_db(username)
    if not db: return True

    # set up values
    if not color: color = 'white'
    if not status: status = DB_STATUS['available']

    # build sql query and commit
    db['cur'].execute('''\
        INSERT INTO notes (username, title, content, color, status)
        VALUES (?,?,?,?,?)''',
        (username, title, content, color, status)
    )
    db['con'].commit()
    db['con'].close()
    return True


def edit_note(username, note_id, title=False, content=False, color=False, status=False):
    sql = 'SELECT title,content,color,status FROM notes WHERE note_id = ?', (note_id,)
    note = query_db(username, sql)

    # if no values were specified for these parameters, we just set the
    # value to whats already there
    if not title: title = note[0]
    if not content: content = note[1]
    if not color: color = note[2]
    if not status: status = note[3]

    # here we update the database
    insert_sql = '''\
        UPDATE notes
        SET title=?, content=?, color=?, status=?
        WHERE note_id=?''', (title, content, color, status, note_id)
    result = query_db(username, sql)
    return True


def archive_note(username, note_id, status='completed'):
    return True


def permanently_delete_note(username, note_id):
    return True


# TODO: Categories?
def insert_note(username, title, text, color):
    return True


# create the 'notes' table if it does not exist
def create_note_db_table(username):
    db = get_note_db(username)
    sql = open('sql/create_table_notes.sql', 'r').read()
    db['cur'].execute(sql)
    db['con'].commit()
    db['cur'].close()
    return True


def get_note_db(username):
    con = sql.connect(get_note_db_name(username))
    if not con: return False
    cur = con.cursor()
    return { 'con': con, 'cur': cur }


def get_note_db_name(username):
    db_path = "user_db/" + str(username) + "_tasks.db"
    return db_path


def query_db(username, query):
    db = get_note_db(username)
    sql = query
    db['cur'].execute(sql)
    result = db['cur'].fetchall()
    db['con'].close()
    return result
