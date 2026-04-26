'''
This is the second version on the grade analyzer, This version in addition to what the first version achieved, creates a 
graph in addition to the summary, and has a home page as well.'''

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageTk  # Imports PIL so images can be used

root = tk.Tk()
root.geometry("600x600")

# ---------------- Storage For User Data ----------------
grades = []

# ---------------- Switching Frames ----------------
def show_frame(frame):
    frame.tkraise()

# ---------------- Process Input ----------------
def process_input():
    global grades
    try:
        # turns the users input e.g. "50,60,70" into [50, 60, 70] so it can be updated into the storage
        grades = list(map(float, entry.get().split(",")))

        # Checking if any grade is above 100
        for grade in grades:
            if grade > 100:
                messagebox.showerror("Error", "Grades cannot be over 100")
                return

        show_frame(ask_sum_frame)
    except ValueError:
        messagebox.showerror("Error", "Please enter numbers separated by commas") # Messagebox.showerror() shows a little pop-up image for the user if their imput is wrong (Not Float)

# ---------------- Calculate Summary ----------------
def generate_summary():
    if not grades:
        summary_label.config(text="No data entered")
        return

    highest = max(grades)
    lowest = min(grades)
    average = sum(grades) / len(grades)

    sorted_grades = sorted(grades)
    n = len(sorted_grades)

    # median calculation
    if n % 2 == 1:
        median = sorted_grades[n // 2]
    else:
        median = (sorted_grades[n//2 - 1] + sorted_grades[n//2]) / 2

    summary_text = (
        f"Highest: {highest}\n"
        f"Lowest: {lowest}\n"
        f"Average: {average:.2f}\n"
        f"Median: {median}"
    )

    summary_label.config(text=summary_text)

# ---------------- Graph ----------------
def show_graph(): # Show graph creates a graph based on the users data, where each dot is one grade. This helps the user have A visual representation.
    if not grades:
        return

    plt.plot(grades, marker="o")
    plt.title("Grades Graph")
    plt.xlabel("Student Number") # Labels the graphs x axis 
    plt.ylabel("Grade")
    plt.show()

# ---------------- Frames ----------------
home_frame = tk.Frame(root)
input_frame = tk.Frame(root)
ask_sum_frame = tk.Frame(root)
summary_frame = tk.Frame(root)

for frame in (home_frame, input_frame, ask_sum_frame, summary_frame):
    frame.place(relwidth=1, relheight=1) # Sets the frames relative width to 1

# ---------------- Home Page ----------------
tk.Label(home_frame, text="Grade Analyzer", font=("Arial", 20)).pack(pady=20)

# Loads and resizes the welcome image for the home page
img1 = Image.open("welcome.png")
img1 = img1.resize((500, 300))
photo1 = ImageTk.PhotoImage(img1)

# Displays the image
tk.Label(home_frame, image=photo1).pack()

tk.Button(home_frame, text="Start",
          command=lambda: show_frame(input_frame)).pack()

# Keeps the image stored so it does not disappear,
home_frame.image = photo1

# ---------------- Input Page ----------------
tk.Label(input_frame, text="Enter grades (comma separated)").pack()

entry = tk.Entry(input_frame)
entry.pack()

tk.Button(input_frame, text="Submit",
          command=process_input).pack()

tk.Button(input_frame, text="Back",
          command=lambda: show_frame(home_frame)).pack()

# ---------------- Key Summary ----------------
tk.Label(input_frame, text="Grading Key:\n<25 = Not Achieved\n25-49 = Achieved\n50-74 = Merit\n75-100 = Excellence").pack(side="bottom")

# ---------------- Asks Summary ----------------
tk.Label(ask_sum_frame, text="Would you like a summary?").pack()

tk.Button(ask_sum_frame, text="Yes",
          command=lambda: [generate_summary(), show_frame(summary_frame)]).pack()

tk.Button(ask_sum_frame, text="No",
          command=lambda: show_frame(home_frame)).pack()

# ---------------- Summary Page ----------------
summary_label = tk.Label(summary_frame, text="")
summary_label.pack()

tk.Button(summary_frame, text="Show Graph",
          command=show_graph).pack()

tk.Button(summary_frame, text="Back to Home",
          command=lambda: show_frame(home_frame)).pack()

# ---------------- Starts the Program --------------------
show_frame(home_frame)
root.mainloop()