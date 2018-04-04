"""
Database Model interface for the COMP249 Web Application assignment

@author: steve cassidy
"""


def position_list(db, limit=10):
    """Return a list of positions ordered by date
    db is a database connection
    return at most limit positions (default 10)

    Returns a list of tuples  (id, timestamp, owner, title, location, company, description)
    """

    sql = """
            SELECT id, timestamp, owner, title, location, company, description
            FROM positions
            ORDER BY timestamp DESC
            LIMIT ?
            """

    c = db.cursor()
    res = []
    for row in c.execute(sql, (limit, )):
        res.append(row)
    return res


def position_get(db, id):
    """Return the details of the position with the given id
    or None if there is no position with this id

    Returns a tuple (id, timestamp, owner, title, location, company, description)

    """

    sql = """
            SELECT id, timestamp, owner, title, location, company, description
            FROM positions
            WHERE id = ?
            """
    c = db.cursor()
    c.execute(sql, (id,))
    return c.fetchone()


def position_add(db, usernick, title, location, company, description):
    """Add a new post to the database.
    The date of the post will be the current time and date.
    Only add the record if usernick matches an existing user

    Return True if the record was added, False if not."""

    c = db.cursor()
    c.execute("""SELECT count(*) FROM users WHERE nick = ?""", (usernick,))
    data = c.fetchone()[0]

    if data == 0:
        return False
    else:
        sql = """
                INSERT INTO positions (owner, title, location, company, description)
                VALUES (?, ?, ?, ?, ?)
                """

        c.execute(sql, (usernick, title, location, company, description))
        db.commit()
        return True
