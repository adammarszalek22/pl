from purehash import *
import sqlite3

'''
NOT NEEDED
'''

def on_entry():
    conn = sqlite3.connect('login.db')
    c = conn.cursor()
    c.execute("CREATE TABLE if not exists passwords(login, hash, login_status)")
    a = c.execute("SELECT * FROM passwords").fetchall()
    for i in a:
        print(i)
    conn.commit()
    conn.close()

def does_login_exist(login):
    conn = sqlite3.connect('login.db')
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM passwords where login = ?", (login,)).fetchone()[0]
        conn.commit()
        conn.close()
        return True
    except TypeError:
        conn.commit()
        conn.close()
        return False

    
def create_user(login, password):
    hash = sha256(password.encode('utf-8')).hexdigest()
    conn = sqlite3.connect('login.db')
    c = conn.cursor()
    c.execute("INSERT INTO passwords VALUES (?, ?, ?)", (login, hash, 'no'))
    conn.commit()
    conn.close()

def check_password(login, password):
    conn = sqlite3.connect('login.db')
    c = conn.cursor()
    try:
        db_hash = c.execute("SELECT * FROM passwords where login = ?", (login,)).fetchone()[1]
    except TypeError:
        return 'Username does not exist'
    conn.commit()
    conn.close()
    hash = sha256(password.encode('utf-8')).hexdigest()
    return hash == db_hash

def compare_two_passwords(password1, password2):
    hash = sha256(password1.encode('utf-8')).hexdigest()
    hash2 = sha256(password2.encode('utf-8')).hexdigest()
    return hash == hash2

on_entry()

