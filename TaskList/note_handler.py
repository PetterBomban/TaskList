import sqlite3 as sql
import user_handler
import os
from flask import session
import bleach

# used for escaping bad html
cleaner = bleach.Cleaner()

DB_STATUS = {'available': 1, 'archived': 2}


def get_notes(username, get_archived=False, get_only_archived=False):
    db = get_note_db(username)

    # doesn't make any sense to allow both..
    if get_archived and get_only_archived:
        get_only_archived = False

    # by default, we do not get archived notes.
    if get_archived:
        sql = 'SELECT title,content,color,note_id FROM notes ORDER BY note_id desc'
    elif get_only_archived:
        sql = '''SELECT title,content,color,note_id
                FROM notes
                WHERE status = 2
                ORDER BY note_id desc'''
    else:
        sql = '''SELECT title,content,color,note_id
                FROM notes
                WHERE status = 1
                ORDER BY note_id desc'''

    db['cur'].execute(sql)
    notes = db['cur'].fetchall()
    db['con'].close()
    return notes


# creates a note database for the current user like so: username_tasks.db
def new_note(username, title, content, color, status=DB_STATUS['available']):
    # check for users' note database
    db = get_note_db(username)
    if not db: return False

    # sanitize html
    for text in content:
        allowed_tags = bleach.ALLOWED_TAGS
        custom_allowed_tags = allowed_tags + ['img']
        allowed_attributes = bleach.ALLOWED_ATTRIBUTES
        custom_allowed_attributes = allowed_attributes['img'] = 'src'
        content = bleach.clean(content, custom_allowed_tags)
    for text in title:
        # sanitize and remove ALL tags from title.
        title = bleach.clean(title, [], [], [], [], True)

    # allow linebreaks
    content = content.replace('\n', '<br/>')

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
    sql = 'SELECT title,content,color,status FROM notes WHERE note_id = ?'
    note = query_db(username, sql, (note_id,))

    # if no values were specified for these parameters, we just set the
    # value to whats already there
    if not title: title = note[0][0]
    if not content: content = note[0][1]
    if not color: color = note[0][2]
    if not status: status = note[0][3]

    # here we update the database
    sql = '''\
        UPDATE notes
        SET title=?, content=?, color=?, status=?
        WHERE note_id=?
        '''
    values = (title, content, color, status, note_id)
    result = update_db(username, sql, values)
    return True


def archive_note(username, note_id):
    edit_note(username, note_id, False, False, False, DB_STATUS['archived'])
    return True


def restore_note(username, note_id):
    edit_note(username, note_id, False, False, False, DB_STATUS['available'])
    return True


def permanently_delete_note(username, note_id):
    sql = 'DELETE FROM notes WHERE note_id=?'
    values = (note_id,)
    result = update_db(username, sql, values)
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


def update_db(username, query, args=None):
    db = get_note_db(username)
    db['cur'].execute(query, args)
    db['con'].commit()
    db['con'].close()
    return True

def query_db(username, query, args=None):
    db = get_note_db(username)
    db['cur'].execute(query, args)
    result = db['cur'].fetchall()
    db['con'].close()
    return result
