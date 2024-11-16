
import mysql.connector
import hashlib

def register(username, password, role):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="******",
            database="online_exam"
        )
        cursor = connection.cursor()

        add_user_query = (
            "INSERT INTO users (username, password, role) "
            "VALUES (%s, %s, %s)"
        )
        cursor.execute(add_user_query, (username, hashed_password, role))

        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()


def authenticate(username, password, role):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="******",
            database="online_exam"
        )
        cursor = connection.cursor()

        auth_query = (
            "SELECT * FROM users WHERE username = %s AND password = %s AND role = %s"
        )
        cursor.execute(auth_query, (username, hashed_password, role))
        user = cursor.fetchone()

        return user is not None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()


