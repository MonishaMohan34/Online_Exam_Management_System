import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import auth
import exam
import management

from tkinter import Canvas
from PIL import Image, ImageTk
# Global variables
correct_answers = []  # Store correct answers globally
exam_window = None  # Define exam_window globally
def register_user():
    username = entry_username.get()
    password = entry_password.get()
    role = combo_role.get()
    if auth.register(username, password, role):
        messagebox.showinfo("Success", "Registration successful!")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Registration failed. Please try again.")

def login():

    username = entry_username.get()
    password = entry_password.get()
    role = combo_role.get()
    if auth.authenticate(username, password, role):
        messagebox.showinfo("Success", f"Login successful as {role}!")
        if role == "Student":
            display_available_exams_page()
        elif role == "Teacher":
            display_teacher_dashboard(username)
        elif role == "Admin":
            display_admin_dashboard()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def display_available_exams_page():
    root.destroy()
    global exam_window
    exam_window = tk.Tk()
    exam_window.title("Available Exams")
    exam_window.configure(bg="white")

    frame_available_exams = tk.Frame(exam_window)
    frame_available_exams.pack(padx=50, pady=30)
    tk.Label(frame_available_exams, text="Available Exams:").pack()
    global listbox_available_exams
    listbox_available_exams = tk.Listbox(frame_available_exams, height=5, width=50)
    listbox_available_exams.pack()
    display_available_exams()

    tk.Button(exam_window, text="Start Exam", bg="green", fg="white",command=start_exam).pack(pady=30)
    tk.Button(exam_window, text="Logout", bg="red", fg="white" ,command=exam_window.destroy).pack(pady=20)

    exam_window.mainloop()

def display_available_exams():
    available_exams = exam.get_available_exams()
    listbox_available_exams.delete(0, tk.END)
    if available_exams:
        for exam_id, exam_name, start_time, end_time, exam_date, subject_name in available_exams:
            exam_info = f"{exam_name} ({subject_name}) - {exam_date} from {start_time} to {end_time}"
            listbox_available_exams.insert(tk.END, exam_info)
    else:
        listbox_available_exams.insert(tk.END, "No available exams")

def display_teacher_dashboard(username):
    root.destroy()
    teacher_window = tk.Tk()
    teacher_window.title("Teacher Dashboard")
    teacher_window.configure(bg="white")
    tk.Label(teacher_window, text="Teacher Dashboard").pack(padx=50, pady=30)
    tk.Button(teacher_window, text="Add Exam",  bg="green", fg="white",command=lambda: add_exam(username)).pack(pady=10)
    tk.Button(teacher_window, text="View My Exams", bg="green", fg="white",command=lambda: view_my_exams(username)).pack(pady=10)
    tk.Button(teacher_window, text="View Exams",bg="green", fg="white", command=lambda: view_exams(username, teacher_window)).pack(pady=10)
    tk.Button(teacher_window, text="Logout", bg="red", fg="white",command=teacher_window.destroy).pack(pady=10)
    teacher_window.mainloop()

def view_my_exams(username):
    exams_window = tk.Toplevel()
    exams_window.title("My Exams")
    exams_window.configure(bg="white")
    frame_my_exams = tk.Frame(exams_window)
    frame_my_exams.pack(padx=50, pady=30)
    tk.Label(frame_my_exams, text="My Exams:").pack()
    listbox_my_exams = tk.Listbox(frame_my_exams, height=5, width=50)
    listbox_my_exams.pack()
    my_exams = exam.get_exams_by_creator(username)
    if my_exams:
        for exam_id, exam_name, start_time, end_time, exam_date, subject_name in my_exams:
            exam_info = f"{exam_name} ({subject_name}) - {exam_date} from {start_time} to {end_time}"
            listbox_my_exams.insert(tk.END, exam_info)
    else:
        listbox_my_exams.insert(tk.END, "No exams found")

    tk.Button(exams_window, text="Close", bg="blue", fg="white",command=exams_window.destroy).pack(pady=10)

def select_exam(username, listbox_available_exams, view_exams_window, teacher_window):
    selected_index = listbox_available_exams.curselection()
    if selected_index:
        selected_exam = listbox_available_exams.get(selected_index)
        exam_name = selected_exam.split(" (")[0]
        exam_id = exam.get_exam_id(exam_name)
        view_exams_window.destroy()
        add_questions(username, exam_id, teacher_window)
    else:
        messagebox.showerror("Error", "Please select an exam")

def add_questions(username, exam_id, teacher_window):
    add_questions_window = tk.Toplevel()
    add_questions_window.title("Add Questions")
    add_questions_window.configure(bg="white")
    tk.Label(add_questions_window, text=f"Add Questions for Exam ID: {exam_id}").pack(pady=10)
    tk.Button(add_questions_window, text="Set Questions", bg="green", fg="white",command=lambda: set_questions(exam_id)).pack(pady=10)
    tk.Button(add_questions_window, text="Close",bg="blue", fg="white", command=add_questions_window.destroy).pack(pady=10)

def display_admin_dashboard():
    root.destroy()
    admin_window = tk.Tk()
    admin_window.title("Admin Dashboard")
    admin_window.configure(bg="white")
    tk.Label(admin_window, text="Admin Dashboard").pack(padx=50, pady=30)
    tk.Button(admin_window, text="Add Exam", bg="green", fg="white",command=add_exam).pack(pady=10)
    tk.Button(admin_window, text="Logout",bg="red", fg="white", command=admin_window.destroy).pack(pady=10)
    admin_window.mainloop()

def add_exam(creator_username=None):
    add_exam_window = tk.Toplevel()
    add_exam_window.title("Add Exam")
    add_exam_window.configure(bg="white")
    tk.Label(add_exam_window, text="Exam Name:").grid(row=0, column=0, padx=5, pady=5)
    entry_exam_name = tk.Entry(add_exam_window)
    entry_exam_name.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(add_exam_window, text="Start Time:").grid(row=1, column=0, padx=5, pady=5)
    entry_start_time = tk.Entry(add_exam_window)
    entry_start_time.grid(row=1, column=1, padx=5, pady=5)
    tk.Label(add_exam_window, text="End Time:").grid(row=2, column=0, padx=5, pady=5)
    entry_end_time = tk.Entry(add_exam_window)
    entry_end_time.grid(row=2, column=1, padx=5, pady=5)
    tk.Label(add_exam_window, text="Exam Date:").grid(row=3, column=0, padx=5, pady=5)
    entry_exam_date = tk.Entry(add_exam_window)
    entry_exam_date.grid(row=3, column=1, padx=5, pady=5)
    tk.Label(add_exam_window, text="Subject Name:").grid(row=4, column=0, padx=5, pady=5)
    entry_subject_name = tk.Entry(add_exam_window)
    entry_subject_name.grid(row=4, column=1, padx=5, pady=5)
    def save_exam():
        exam_name = entry_exam_name.get()
        start_time = entry_start_time.get()
        end_time = entry_end_time.get()
        exam_date = entry_exam_date.get()
        subject_name = entry_subject_name.get()
        if creator_username:
            success = exam.add_exam(exam_name, start_time, end_time, exam_date, subject_name, creator_username)
        else:
            success = exam.add_exam(exam_name, start_time, end_time, exam_date, subject_name)
        if success:
            messagebox.showinfo("Success", "Exam added successfully!")
            add_exam_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to add exam. Please try again.")
    tk.Button(add_exam_window, text="Save Exam", bg="green", fg="white",command=save_exam).grid(row=5, columnspan=2, pady=10)

def view_exams(username, teacher_window):
    view_exams_window = tk.Toplevel()
    view_exams_window.title("View Exams")
    view_exams_window.configure(bg="white")
    frame_available_exams = tk.Frame(view_exams_window)
    frame_available_exams.pack(padx=50, pady=30)
    tk.Label(frame_available_exams, text="Available Exams:").pack()
    listbox_available_exams = tk.Listbox(frame_available_exams, height=5, width=50)
    listbox_available_exams.pack()
    display_available_exams_for_teacher(username, listbox_available_exams)
    tk.Button(view_exams_window, text="Select Exam", bg="green", fg="white",command=lambda: select_exam(username, listbox_available_exams, view_exams_window, teacher_window)).pack(pady=10)
    tk.Button(view_exams_window, text="Close", bg="blue", fg="white",command=view_exams_window.destroy).pack(pady=10)

def display_available_exams_for_teacher(username, listbox_available_exams):
    my_exams = exam.get_exams_by_creator(username)
    #root.configure(bg="white")
    listbox_available_exams.delete(0, tk.END)
    if my_exams:
        for exam_id, exam_name, start_time, end_time, exam_date, subject_name in my_exams:
            exam_info = f"{exam_name} ({subject_name}) - {exam_date} from {start_time} to {end_time}"
            listbox_available_exams.insert(tk.END, exam_info)
    else:
        listbox_available_exams.insert(tk.END, "No exams found")

def start_exam():
    selected_index = listbox_available_exams.curselection()
    if selected_index:
        selected_exam = listbox_available_exams.get(selected_index)
        exam_name = selected_exam.split(" (")[0]
        exam_id = exam.get_exam_id(exam_name)
        take_exam(exam_id)
    else:
        messagebox.showerror("Error", "Please select an exam")

correct_answers = None
# Function to reinitialize correct_answers as an empty list
def initialize_correct_answers():
    global correct_answers
    correct_answers = []

initialize_correct_answers()

def take_exam(exam_id):
    global exam_window
    exam_window.destroy()
    exam_window = tk.Tk()
    exam_window.title("Take Exam")
    exam_window.configure(bg="white")
    questions = exam.get_questions_by_exam_id(exam_id)
    correct_answers.clear()
    frame_questions = tk.Frame(exam_window)
    frame_questions.pack(padx=75, pady=60)
    if questions:
        for idx, (question, correct_answer) in enumerate(questions, 1):
            tk.Label(frame_questions, text=f"Q{idx}. {question}").pack(anchor='w')
            entry_answer = tk.Entry(frame_questions)
            entry_answer.pack(anchor='w')
            correct_answers.append((entry_answer, correct_answer))
        tk.Button(exam_window, text="Submit",bg="green", fg="white", command=submit_exam).pack(pady=10)
    else:
        tk.Label(exam_window, text="No questions found for this exam.").pack()
    exam_window.mainloop()

def submit_exam():
    global exam_window, correct_answers  # Use the global variables
    if exam_window:
        # Initialize a list to store user answers
        user_answers = []
        # Iterate through each question frame in the exam window
        for frame in exam_window.winfo_children():
            if isinstance(frame, tk.Frame):
                # Find the selected option for the current question
                selected_option = None
                for idx, child in enumerate(frame.winfo_children()):
                    if isinstance(child, tk.Radiobutton) and child.get() == 1:
                        selected_option = idx + 1  # Add 1 to match option indexing (starting from 1)
                # Append the selected option to the user_answers list
                user_answers.append(selected_option)
        # Process the user answers
        process_user_answers(user_answers)
    else:
        messagebox.showerror("Error", "Exam window not defined.")

def process_user_answers(user_answers):
    global correct_answers  # Use the global correct_answers
    # Example: Calculate score
    num_correct = sum(1 for user_ans, correct_ans in zip(user_answers, correct_answers) if user_ans == correct_ans)
    messagebox.showinfo("Exam Status",f'Submitted Successfully and Results will be announced later')



def set_questions(exam_id):
    set_questions_window = tk.Toplevel()
    set_questions_window.title("Set Questions")
    set_questions_window.configure(bg="white")
    tk.Label(set_questions_window, text=f"Set Questions for Exam ID: {exam_id}").pack(pady=10)
    frame_questions = tk.Frame(set_questions_window)
    frame_questions.pack(padx=50, pady=30)
    entries = []
    def add_question_entry():
        question_frame = tk.Frame(frame_questions)
        question_frame.pack(pady=5, fill='x')
        tk.Label(question_frame, text="Question:").pack(side='left')
        entry_question = tk.Entry(question_frame, width=50)
        entry_question.pack(side='left', padx=5)
        tk.Label(question_frame, text="Answer:").pack(side='left')
        entry_answer = tk.Entry(question_frame, width=20)
        entry_answer.pack(side='left', padx=5)
        entries.append((entry_question, entry_answer))

    def save_questions():
        questions_and_answers = [(entry_q.get(), int(entry_a.get())) for entry_q, entry_a in entries]
        success = exam.save_questions(exam_id, questions_and_answers)
        if success:
            messagebox.showinfo("Success", "Questions set successfully!")
            set_questions_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to set questions. Please try again.")

    tk.Button(set_questions_window, text="Add Question", bg="green", fg="white",command=add_question_entry).pack(pady=10)
    tk.Button(set_questions_window, text="Save Questions", bg="green", fg="white",command=save_questions).pack(pady=10)

    add_question_entry()

def logout():
    root.destroy()
    display_login_page()

def display_login_page():
    global root
    root = tk.Tk()
    root.title("Exam Management System")
    def resize_bg(event):
        new_width = event.width
        new_height = event.height
        image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        background_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=background_image, anchor="nw")
        canvas.image = background_image  # Keep a reference to prevent garbage collection

# Load the background image
    original_image = Image.open("Image/login1.jpg")
    background_image = ImageTk.PhotoImage(original_image)

# Create a Canvas widget
    canvas = Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)

# Display the background image on the canvas
    canvas.create_image(0, 0, image=background_image, anchor="nw")
    canvas.image = background_image

# Bind the resize event to the resize_bg function
    root.bind('<Configure>', resize_bg)
    #login_frame = tk.Frame(root, bg='white', padx=20, pady=20, relief='ridge', bd=2)
    frame_login = tk.Frame(root, bg='white', padx=20, pady=20, relief='ridge', bd=2)
    #frame_login.pack(padx=250, pady=150)
    frame_login.place(relx=0.5, rely=0.5, anchor='center')
    tk.Label(frame_login, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    global entry_username
    entry_username = tk.Entry(frame_login)
    entry_username.grid(row=0, column=1, padx=10, pady=10)
    tk.Label(frame_login, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    global entry_password
    entry_password = tk.Entry(frame_login, show='*')
    entry_password.grid(row=1, column=1, padx=10, pady=10)
    tk.Label(frame_login, text="Role:").grid(row=2, column=0, padx=10, pady=10)
    global combo_role
    combo_role = ttk.Combobox(frame_login, values=["Student", "Teacher", "Admin"])
    combo_role.grid(row=2, column=1, padx=10, pady=10)
    combo_role.current(0)
    tk.Button(frame_login, text="Register", bg="green", fg="white",command=register_user).grid(row=3, column=0, padx=15, pady=20)
    tk.Button(frame_login, text="Login", bg="green", fg="white",command=login).grid(row=3, column=1, padx=15, pady=20)
    root.mainloop()

display_login_page()