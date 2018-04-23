"""
Created on Mar 26, 2012

@author: steve
"""
from bottle import response, request
import database
import uuid
# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'


def check_login(db, usernick, password):
    """returns True if password matches stored"""

    hash = database.password_hash(password)

    sql = """
    SELECT password
    FROM users
    WHERE nick=?;
    """

    c = db.cursor()
    c.execute(sql,(usernick,))
    stored = c.fetchone()

    if stored is not None and hash == stored[0]:
        return True
    else:
        return False


def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """

    #Check if usernick is a valid user
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE nick = ?", (usernick,))
    stored = c.fetchone()

    if stored is None:
        return None

    #Check if usernick already has an active session
    c.execute("SELECT * FROM sessions WHERE usernick = ?",(usernick,))
    session = c.fetchone()

    if session is None:
        #create a new session
        sessionid = str(uuid.uuid4())
        c.execute("INSERT INTO sessions VALUES (?,?)", (sessionid, usernick))
    else:
        #retrieve exisiting sessionid
        c.execute("SELECT sessionid FROM sessions WHERE usernick = ?",(usernick,))
        sessionid = c.fetchone()[0]

    response.set_cookie(COOKIE_NAME, sessionid)
    return sessionid


def delete_session(db, usernick):
    """remove all session table entries for this user"""

    c = db.cursor()
    c.execute("DELETE FROM sessions WHERE usernick = ?", (usernick,))


def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""

    sessionid = request.get_cookie(COOKIE_NAME)

    #find and return existing sessionid else return none
    c = db.cursor()
    c.execute("SELECT usernick FROM sessions WHERE sessionid = ?", (sessionid,))
    usernick = c.fetchone()

    if usernick is None:
        return None
    else:
        return usernick[0]