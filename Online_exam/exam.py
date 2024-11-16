
import mysql.connector

def add_exam(exam_name, start_time, end_time, exam_date, subject_name, creator_username=None):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="******",  
            database="online_exam"
        )
        cursor = conn.cursor()

        if creator_username:
            query = """
            INSERT INTO Exams (exam_name, start_time, end_time, exam_date, subject_name, creator_username)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (exam_name, start_time, end_time, exam_date, subject_name, creator_username)
        else:
            query = """
            INSERT INTO Exams (exam_name, start_time, end_time, exam_date, subject_name)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (exam_name, start_time, end_time, exam_date, subject_name)

        cursor.execute(query, values)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_available_exams():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="******",
            database="online_exam"
        )
        cursor = connection.cursor()

        get_exams_query = "SELECT exam_id, exam_name, start_time, end_time, exam_date, subject_name FROM exams"
        cursor.execute(get_exams_query)
        exams = cursor.fetchall()

        return exams
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_exams_by_creator(creator_username):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="******",
            database="online_exam"
        )
        cursor = connection.cursor()

        get_exams_query = "SELECT exam_id, exam_name, start_time, end_time, exam_date, subject_name FROM exams WHERE creator_username = %s"
        cursor.execute(get_exams_query, (creator_username,))
        exams = cursor.fetchall()

        return exams
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_exam_id(exam_name):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="******",
            database="online_exam"
        )
        cursor = connection.cursor()

        get_exam_id_query = "SELECT exam_id FROM exams WHERE exam_name = %s"
        cursor.execute(get_exam_id_query, (exam_name,))
        exam_id = cursor.fetchone()

        return exam_id[0] if exam_id else None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_exam_questions(exam_id):
    # Placeholder implementation to simulate fetching exam questions from a database or other source
    if exam_id == 1:
        return [("Question 1", "Option 1", "Option 2", "Option 3", "Option 4", 1),  # Sample question with correct option at index 1
                ("Question 2", "Option 1", "Option 2", "Option 3", "Option 4", 2),  # Sample question with correct option at index 2
                # Add more questions here
               ]
    else:
        return None 
    
def get_questions_by_exam_id(exam_id):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="******",
            database="online_exam"
        )
        cursor = connection.cursor()

        # Query to retrieve questions for the given exam_id
        query = "SELECT question_text, correct_answer_index FROM questions WHERE exam_id = %s"
        cursor.execute(query, (exam_id,))
        questions_data = cursor.fetchall()

        # Format the data as a list of tuples (question_text, correct_answer_index)
        questions = [(question_text, correct_answer_index) for question_text, correct_answer_index in questions_data]

        return questions
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def save_questions(exam_id, questions_and_answers):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="******",
            database="online_exam"
        )
        cursor = connection.cursor()

        for question_text, correct_answer_index in questions_and_answers:
            query = """
            INSERT INTO questions (exam_id, question_text, correct_answer_index)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (exam_id, question_text, correct_answer_index))

        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


