'''
This is the fourth Version of the grade analyzer code. This version adds the option to export the failed
students into an external file, which is created on the users computer.
'''

import tkinter as tk
from tkinter import messagebox, filedialog # fileddialog lets the user choose where to put the file (so they don't need a pre-created file)
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import csv # csv creates a spreadsheet for those failed grades.

root = tk.Tk()
root.geometry("600x600")

# ---------------- Storage For User Data ----------------
data = []

# ---------------- Switching Frames ----------------
def show_frame(frame):
    frame.tkraise()

# ---------------- Process Input ----------------
def process_input():
    global data
    try:
        entries = entry.get().split(",")
        data = []

        for item in entries:
            name, grade = item.split(":")
            grade = float(grade)

            # Validation
            if grade > 100:
                messagebox.showerror("Error", "Grades cannot be over 100")
                return # Puts a maximum grade as 100

            if grade < 0:
                messagebox.showerror("Error", "Grades cannot be negative") # Catches negative grade error
                return

            data.append((name.strip(), grade))

        show_frame(select_frame)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter data like name:grade,name:grade (e.g. Alex:75,Bob:60)"
        ) # Input validation message, helps the user as well

# ---------------- Generating Summary ----------------
def generate_selected_summary():
    if not data:
        summary_label.config(text="No data entered")
        return # Creates the summary based on the users data

    result = ""

    grades = [g for n, g in data]
    highest = max(data, key=lambda x: x[1])
    lowest = min(data, key=lambda x: x[1])
    average = sum(grades) / len(grades) # These options are checkboxes, so the user can pick and choose what they want.

    sorted_grades = sorted(grades)
    n = len(sorted_grades)

    if n % 2 == 1:
        median = sorted_grades[n // 2]
    else:
        median = (sorted_grades[n//2 - 1] + sorted_grades[n//2]) / 2

    if highest_var.get():
        result += f"Highest: {highest[0]} ({highest[1]})\n"

    if lowest_var.get():
        result += f"Lowest: {lowest[0]} ({lowest[1]})\n"

    if average_var.get():
        result += f"Average: {average:.2f}\n"

    if median_var.get():
        result += f"Median: {median}\n"

    if result == "":
        result = "No options selected"

    summary_label.config(text=result)

# ---------------- Exporting fail grades ----------------
def export_failed_students():
    if not data: # This function exports the names (and grades) of students who scored under 25 (not achieved)
        messagebox.showerror("Error", "No data to export")
        return

    failed = [(name, grade) for name, grade in data if grade < 25]

    if not failed:
        messagebox.showinfo("Info", "No students failed (Not Achieved)") # Error trapping - if no students failed it prints a message
        return

    file_path = filedialog.asksaveasfilename( #Sends the data to the file created
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        return

    try:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Grade"])
            writer.writerows(failed)

        messagebox.showinfo("Success", f"{len(failed)} students exported successfully")

    except Exception as e:
        messagebox.showerror("Error", f"Could not write file: {e}")

# ---------------- Graph ----------------
def show_graph():
    if not data:
        return

    names = [n for n, g in data]
    grades = [g for n, g in data]

    plt.figure()
    plt.plot(names, grades, marker="o")
    plt.title("Grades Graph")
    plt.xlabel("Students")
    plt.ylabel("Grade")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()

# ---------------- Frames ----------------
home_frame = tk.Frame(root)
input_frame = tk.Frame(root)
select_frame = tk.Frame(root)
summary_frame = tk.Frame(root)

for frame in (home_frame, input_frame, select_frame, summary_frame):
    frame.place(relwidth=1, relheight=1)

# ---------------- Home Page ----------------
tk.Label(home_frame, text="Grade Analyzer", font=("Arial", 20)).pack(pady=20)

img1 = Image.open("welcome.png")
img1 = img1.resize((500, 300)) # Resizes the homepage welcome image so its larger, creating a more grandoise effect.
photo1 = ImageTk.PhotoImage(img1)

tk.Label(home_frame, image=photo1).pack()

tk.Button(home_frame, text="Start",
          command=lambda: show_frame(input_frame)).pack()

home_frame.image = photo1

# ---------------- Input Page ----------------
tk.Label(input_frame, text="Enter data (name:grade, comma separated)").pack()

entry = tk.Entry(input_frame)
entry.pack()

tk.Button(input_frame, text="Submit", 
          command=process_input).pack()

tk.Button(input_frame, text="Back",
          command=lambda: show_frame(home_frame)).pack()

tk.Label(
    input_frame,
    text="Grading Key:\n<25 = Not Achieved\n25-49 = Achieved\n50-74 = Merit\n75-100 = Excellence" # Provides users with a key for simplicity.
).pack(side="bottom")

# ---------------- Selection Page ----------------
tk.Label(select_frame, text="Select what you want to see").pack()

highest_var = tk.BooleanVar()
lowest_var = tk.BooleanVar()
average_var = tk.BooleanVar()
median_var = tk.BooleanVar()

tk.Checkbutton(select_frame, text="Highest", variable=highest_var).pack()
tk.Checkbutton(select_frame, text="Lowest", variable=lowest_var).pack()
tk.Checkbutton(select_frame, text="Average", variable=average_var).pack()
tk.Checkbutton(select_frame, text="Median", variable=median_var).pack() # Sets the summary points as checkboxes for ease of use

tk.Button(select_frame, text="Show Results",
          command=lambda: [generate_selected_summary(), show_frame(summary_frame)]).pack()

tk.Button(select_frame, text="Back",
          command=lambda: show_frame(input_frame)).pack()

# ---------------- Summary Page ----------------
summary_label = tk.Label(summary_frame, text="")
summary_label.pack()

tk.Button(summary_frame, text="Show Graph",
          command=show_graph).pack()

tk.Button(summary_frame, text="Export Failed Students",
          command=export_failed_students).pack()

tk.Button(summary_frame, text="Back to Home",
          command=lambda: show_frame(home_frame)).pack()

# ---------------- Start Program ----------------
show_frame(home_frame)
root.mainloop()