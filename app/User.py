import sqlite3
import hashlib
salt = "this_is_salt"

def getUser(db, username, password):
    temp_password = password+salt
    hash_password = hashlib.md5(temp_password.encode()).hexdigest()
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = "SELECT id FROM users WHERE username=?"
    cursor.execute(sql, [username])
    if cursor.fetchone() == None:
        cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", [username, hash_password])
        conn.commit()
        temp = {'id': cursor.lastrowid, 'username':username, 'last': 0}
    else:
        sql = "SELECT id, username, last FROM users WHERE username=? AND password=?"
        cursor.execute(sql, [username, hash_password])
        temp = cursor.fetchone()
        if temp == None:
            return None
    return temp