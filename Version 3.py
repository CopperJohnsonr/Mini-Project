'''
This is the third version on the grade analyzer, This version builds on the previous one, asking the user what part of the summary they want, 
so that they pick and choose, then are shown what they picked. This is done using checkboxes.
'''

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("600x600")

# ---------------- Storage For User Data ----------------
data = [] # Stores pairs of names and grades

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

            # Sets max grade to 100
            if grade > 100:
                messagebox.showerror("Error", "Grades cannot be over 100")
                return

            if grade < 0:
                messagebox.showerror("Error", "Grades cannot be negative")
                return

            data.append((name, grade))

        show_frame(select_frame)

    except ValueError:
        messagebox.showerror("Error", "Please enter data like name:grade,name:grade (e.g. Alex:75,Bob:60)")

# ---------------- Generating Summary ----------------
def generate_selected_summary():
    if not data:
        summary_label.config(text="No data entered")
        return

    result = ""  # stores chosen results

    grades = [g for n, g in data]

    # calculates values first
    highest = max(data, key=lambda x: x[1])
    lowest = min(data, key=lambda x: x[1])
    average = sum(grades) / len(grades)

    sorted_grades = sorted(grades)
    n = len(sorted_grades)

    if n % 2 == 1:
        median = sorted_grades[n // 2]
    else:
        median = (sorted_grades[n//2 - 1] + sorted_grades[n//2]) / 2

    # only adds what the user selected
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

# ---------------- Graph ----------------
def show_graph():
    if not data:
        return

    grades = [g for n, g in data]

    plt.plot(grades, marker="o")
    plt.title("Grades Graph")
    plt.xlabel("Student Number") 
    '''NEED TO CHANGE THIS THis should be number of students or name or something?'''
    plt.ylabel("Grade")
    plt.show()

# ---------------- Frames ----------------
home_frame = tk.Frame(root)
input_frame = tk.Frame(root)
select_frame = tk.Frame(root) # A select frame for choosing what summary info the user wants
summary_frame = tk.Frame(root)

for frame in (home_frame, input_frame, select_frame, summary_frame):
    frame.place(relwidth=1, relheight=1)

# ---------------- Home Page ----------------
tk.Label(home_frame, text="Grade Analyzer", font=("Arial", 20)).pack(pady=20)

img1 = Image.open("welcome.png")
img1 = img1.resize((500, 300))
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

# ---------------- Key for Summary ----------------
tk.Label(input_frame, text="Grading Key:\n<25 = Not Achieved\n25-49 = Achieved\n50-74 = Merit\n75-100 = Excellence").pack(side="bottom")

# ---------------- Selection Page ----------------
tk.Label(select_frame, text="Select what you want to see").pack()

# Options for checkboxes
highest_var = tk.BooleanVar()
lowest_var = tk.BooleanVar() # BooleanVar is a function that checks whether the checkbox is selected or not. - Found this while browsing the TKinter directory
average_var = tk.BooleanVar()
median_var = tk.BooleanVar()

tk.Checkbutton(select_frame, text="Highest", variable=highest_var).pack() # Checkbutton creates a checkbox available to the user
tk.Checkbutton(select_frame, text="Lowest", variable=lowest_var).pack()
tk.Checkbutton(select_frame, text="Average", variable=average_var).pack()
tk.Checkbutton(select_frame, text="Median", variable=median_var).pack()

tk.Button(select_frame, text="Show Results",
          command=lambda: [generate_selected_summary(), show_frame(summary_frame)]).pack()

tk.Button(select_frame, text="Back",
          command=lambda: show_frame(input_frame)).pack()

# ---------------- Summary Page ----------------
summary_label = tk.Label(summary_frame, text="")
summary_label.pack()

tk.Button(summary_frame, text="Show Graph",
          command=show_graph).pack()

tk.Button(summary_frame, text="Back to Home",
          command=lambda: show_frame(home_frame)).pack()

# ---------------- Start Program ----------------
show_frame(home_frame)
root.mainloop()