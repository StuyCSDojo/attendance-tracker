import sqlite3
import hash

DB_NAME = "admins.db"
CREATE_QUERY = "CREATE TABLE IF NOT EXISTS admins (username text,\
        password_hash text);"
SELECT_QUERY = "SELECT * FROM admins WHERE username = ? AND password_hash = ?;"
LIST_QUERY = "SELECT * FROM admins;"
INSERT_QUERY = "INSERT INTO admins VALUES (?, ?);"
DELETE_QUERY = "DELETE FROM admins WHERE username = ? AND password_hash = ?;"

def init_tables():
    """
    Initializes the database with the admin table if it doesn't exist yet

    Params:
        None

    Returns:
        None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(CREATE_QUERY);
    conn.commit()
    conn.close()
    return

def list_admin():
    """
    Lists all admins

    Params:
        None

    Returns:
        A list of all the admins in the database
    """
    init_tables()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    result = list(c.execute(LIST_QUERY))
    conn.close()
    return result

def admin_exists(username, password):
    """
    Check if an admin with specified username and password exists in the
    database

    Params:
        username - A string containing the admin's username
        password - A string containing the admin's password

    Returns:
        True if the specified admin exists (exactly once) in the database,
        False otherwise
    """
    init_tables()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    PARAMS = (username , hash.password_hash(password))
    result = list(c.execute(SELECT_QUERY, PARAMS))
    conn.close()
    return len(result) == 1 # If > 1, then duplicate users

def add_admin(username, password):
    """
    Adds an admin to the database

    Params:
        username - A string containing the admin's username
        password - A string containing the admin's password

    Returns:
        None
    """
    init_tables()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    PARAMS = (username, hash.password_hash(password))
    c.execute(INSERT_QUERY, PARAMS)
    conn.commit()
    conn.close()
    return

def remove_admin(username, password):
    """
    Removes an admin to the database

    Params:
        username - A string containing the admin's username
        password - A string containing the admin's password

    Returns:
        None
    """
    init_tables()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    PARAMS = (username, hash.password_hash(password))
    c.execute(DELETE_QUERY, PARAMS)
    conn.commit()
    conn.close()
    return

