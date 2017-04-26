import sqlite3 as sql
import user_handler
import os
from flask import session

DB_STATUS = {'available': 1, 'archived': 2}


def get_notes(username):
    db = get_note_db(username)
    sql = 'SELECT title,content,color FROM notes ORDER BY note_id desc'
    db['cur'].execute(sql)
    notes = db['cur'].fetchall()
    db['con'].close()
    print(notes)
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
    return True

