import sqlite3

def on_entry():
    conn = sqlite3.connect('score_guesses.db')
    c = conn.cursor()
    c.execute("CREATE TABLE if not exists guesses(match_id, goal1, goal2)")
    a = c.execute("SELECT * FROM guesses").fetchall()
    for i in a:
        print(i)
    conn.commit()
    conn.close()

def add_guess(match_id, goal1, goal2):
    conn = sqlite3.connect('score_guesses.db')
    c = conn.cursor()
    c.execute("INSERT INTO guesses VALUES (?, ?, ?)", (match_id, goal1, goal2,))
    conn.commit()
    conn.close()

def update_guess(match_id, goal1, goal2):
    conn = sqlite3.connect('score_guesses.db')
    c = conn.cursor()
    c.execute("UPDATE guesses SET goal1 = ?, goal2 = ? WHERE match_id = ?", (goal1, goal2, match_id,))
    conn.commit()
    conn.close()

def delete_guess(match_id):
    conn = sqlite3.connect('score_guesses.db')
    c = conn.cursor()
    c.execute("DELETE FROM guesses WHERE match_id = ?", (match_id,))
    conn.commit()
    conn.close()

def delete_all_guesses():
    conn = sqlite3.connect('score_guesses.db')
    c = conn.cursor()
    c.execute("DELETE FROM guesses")
    conn.commit()
    conn.close()

def get_guess(match_id):
    conn = sqlite3.connect('score_guesses.db')
    c = conn.cursor()
    guess = c.execute("SELECT * FROM guesses WHERE match_id = ?", (match_id,)).fetchone()
    conn.commit()
    conn.close()
    return guess

def get_all_guesses():
    conn = sqlite3.connect('score_guesses.db')
    c = conn.cursor()
    guesses = c.execute("SELECT * FROM guesses").fetchall()
    conn.commit()
    conn.close()
    return guesses