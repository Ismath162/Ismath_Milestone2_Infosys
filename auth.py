import bcrypt
from database import create_connection

def register_user(username, email, password):
    conn = create_connection()
    cursor = conn.cursor()
    
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_pw)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return bcrypt.checkpw(password.encode(), user[0])
    return False