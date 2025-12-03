import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import matplotlib.pyplot as plt

CSV_FILE = "students_data.csv"

# Create CSV file if not exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Mobile", "Course", "Marks", "Gender"])

def submit_data():
    name = entry_name.get().strip()
    mobile = entry_mobile.get().strip()
    course = course_combo.get()
    marks = entry_marks.get().strip()
    gender = gender_var.get()

    if not name or not mobile or not course or not marks or gender == 0:
        messagebox.showinfo("Error", "Please fill all fields!")
        return

    if not mobile.isdigit() or len(mobile) != 10:
        messagebox.showinfo("Error", "Mobile must be 10 digits!")
        return

    try:
        marks = int(marks)
        if not (0 <= marks <= 100):
            raise ValueError
    except:
        messagebox.showinfo("Error", "Marks must be between 0 and 100!")
        return

    gender_text = {1: "Male", 2: "Female", 3: "Others"}[gender]

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, mobile, course, marks, gender_text])

    messagebox.showinfo("Success", "Data saved successfully!")
    
    # Clear form
    entry_name.delete(0, tk.END)
    entry_mobile.delete(0, tk.END)
    entry_marks.delete(0, tk.END)
    course_combo.set("")
    gender_var.set(0)

def analysis_of_marks():
    if not os.path.exists(CSV_FILE) or os.stat(CSV_FILE).st_size == 0:
        messagebox.showinfo("No Data", "No records found!")
        return

    names = []
    marks_list = []

    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            names.append(row["Name"])
            marks_list.append(int(row["Marks"]))

    plt.figure(figsize=(10, 6))
    plt.scatter(marks_list, names, color="green", s=100)
    plt.title("Student Marks Analysis", fontsize=16)
    plt.xlabel("Marks")
    plt.ylabel("Student Name")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ========================= GUI =========================
root = tk.Tk()
root.title("Student Registration System")
root.geometry("800x600")
root.configure(bg="#f0f8ff")

# Title
tk.Label(root, text="STUDENT REGISTRATION FORM", font=("Arial", 20, "bold"), 
         bg="#4a90e2", fg="white", pady=15).pack(fill=tk.X)

frame = tk.Frame(root, bg="#f0f8ff")
frame.pack(pady=30)

# Name
tk.Label(frame, text="Student Name :", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, sticky="w", pady=10, padx=20)
entry_name = tk.Entry(frame, font=("Arial", 12), width=35)
entry_name.grid(row=0, column=1, pady=10, padx=20)

# Mobile
tk.Label(frame, text="Mobile Number :", font=("Arial", 12), bg="#f0f8ff").grid(row=1, column=0, sticky="w", pady=10, padx=20)
entry_mobile = tk.Entry(frame, font=("Arial", 12), width=35)
entry_mobile.grid(row=1, column=1, pady=10, padx=20)

# Course
tk.Label(frame, text="Course :", font=("Arial", 12), bg="#f0f8ff").grid(row=2, column=0, sticky="w", pady=10, padx=20)
course_combo = ttk.Combobox(frame, values=["ECE","CSE","IT","MCA","MECH","CIVIL","EEE","CHEM"], state="readonly", width=32)
course_combo.grid(row=2, column=1, pady=10, padx=20)
course_combo.set("CSE")

# Marks
tk.Label(frame, text="Marks (0-100) :", font=("Arial", 12), bg="#f0f8ff").grid(row=3, column=0, sticky="w", pady=10, padx=20)
entry_marks = tk.Entry(frame, font=("Arial", 12), width=35)
entry_marks.grid(row=3, column=1, pady=10, padx=20)

# Gender - Fixed properly
tk.Label(frame, text="Gender :", font=("Arial", 12), bg="#f0f8ff").grid(row=4, column=0, sticky="w", pady=15, padx=20)

gender_var = tk.IntVar(value=0)

# Put radio buttons in a separate frame so they align nicely
gender_frame = tk.Frame(frame, bg="#f0f8ff")
gender_frame.grid(row=4, column=1, sticky="w", pady=15)

tk.Radiobutton(gender_frame, text="Male",    variable=gender_var, value=1, font=("Arial", 11), bg="#f0f8ff").pack(side=tk.LEFT, padx=20)
tk.Radiobutton(gender_frame, text="Female",  variable=gender_var, value=2, font=("Arial", 11), bg="#f0f8ff").pack(side=tk.LEFT, padx=20)
tk.Radiobutton(gender_frame, text="Others",  variable=gender_var, value=3, font=("Arial", 11), bg="#f0f8ff").pack(side=tk.LEFT, padx=20)

# Buttons
btn_frame = tk.Frame(root, bg="#f0f8ff")
btn_frame.pack(pady=40)

tk.Button(btn_frame, text="SUBMIT", command=submit_data, font=("Arial", 14, "bold"), 
          bg="#4CAF50", fg="white", width=12, height=2).pack(side=tk.LEFT, padx=30)
tk.Button(btn_frame, text="VIEW ANALYSIS", command=analysis_of_marks, font=("Arial", 14, "bold"), 
          bg="#2196F3", fg="white", width=15, height=2).pack(side=tk.LEFT, padx=30)

root.mainloop()