import sqlite3
import os

# Fix 1: Environment variable se key load ho rahi hai (No hardcoded credentials)
SECRET_API_KEY = os.getenv("API_KEY", "DEFAULT_SAFE_ENV_KEY")

def login_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Fix 2: Parameterized query (Prepared Statement) - SQL Injection completely blocked!
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print(f"Executing Safe Query: {query}")
    
    # User inputs ko tuple me as parameters pass kiya ja raha hai
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

if __name__ == "__main__":
    # Safe execution test
    login_user("admin", "safe_password_123")