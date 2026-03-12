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

    cursor.execute("SELECT password, username FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    conn.close()

    if user:
        stored_pw = user[0]
        username = user[1]

        if bcrypt.checkpw(password.encode(), stored_pw):
            return True, username

    return False, None