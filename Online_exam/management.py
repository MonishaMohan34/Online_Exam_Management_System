import mysql.connector
from db import get_connection
def create_exam(exam_name, start_time, end_time, exam_date, subject_name, creator_username):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Exams (exam_name, start_time, end_time, exam_date, subject_name, creator_username)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (exam_name, start_time, end_time, exam_date, subject_name, creator_username))
    connection.commit()
    cursor.close()
    connection.close()


def add_question(exam_id, question_text, option_texts, correct_option_index):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="******",
            database="online_exam"
        )
        cursor = connection.cursor()

        add_question_query = (
            "INSERT INTO questions ( exam_id,question_text) "
            "VALUES ( %s , %s)"
        )
        cursor.execute(add_question_query, (exam_id, question_text))
        question_id = cursor.lastrowid

        add_option_query = (
            "INSERT INTO options (exam_id,question_id, option_text, is_correct) "
            "VALUES (%s,%s, %s, %s)"
        )
        for i, option_text in enumerate(option_texts):
            is_correct = (i == correct_option_index)
            cursor.execute(add_option_query, (question_id, option_text, is_correct))

        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()








