import sqlite3
import os

# Fix 1: Environment Variable se key read karna (No Hardcoded Secrets)
SECRET_API_KEY = os.getenv("API_KEY", "DEFAULT_SAFE_ENV_KEY")

def login_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Fix 2: Parameterized Query / Prepared Statements (SQL Injection Blocked!)
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print(f"Executing Safe Query: {query}")
    
    # Input Values Tuples ke roop me pass ho rahi hain
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

if __name__ == "__main__":
    # Ab SQL Injection Attack kaam nahi karega!
    login_user("admin' OR '1'='1", "password")