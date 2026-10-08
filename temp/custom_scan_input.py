import sqlite3

def login(user, password):
    query = f"SELECT * FROM users WHERE user='{user}'"
    return query