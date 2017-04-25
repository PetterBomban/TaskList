import sqlite3 as sql
import user_handler
from flask import session

# creates a note database for the current user like so: username_tasks.db
def new_note(username, title, text, color='white'):
    # check for users' note database
    if not check_note_db(username):
        create_note_db(username)
    


def edit_note(username, note_id, title=False, text=False, color=False):
    print()


def archive_note(username, note_id, status='completed'):
    return True


def permanently_delete_note(username, note_id):
    return True


# TODO: Categories?
def insert_note(username, title, text, color):
    print()


def create_note_db(username):
    print()


def check_note_db(username):
    return True



