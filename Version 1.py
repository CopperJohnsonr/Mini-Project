'''
This is the first version on the grade analyzer, this version calculates the highest score, lowest
score, the median and average, and sets them all as a summary, which is then asked if the user wants
to see it.
'''
import tkinter as tk # Imports the TKinter module
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("600x600")

# ----------------- Data Storage -----------------
grades = []  # Stores user input

def show_frame(frame): # Raises the frame to the front
    frame.tkraise()

def process_input():
    """This takes the users inputs, makes them numbers and updates them"""
    global grades # Allows the grades to be accessed and update
    try:
        # Allows the input of numbers
        grades = list(map(float, entry.get().split(",")))

    #Checks if any grade is above 100
        for grade in grades:
            if grade > 100:
                result_label.config(text="Grades cannot be over 100")
                return

        show_frame(ask_sum_frame)
    except ValueError:
        result_label.config(text="Please enter valid numbers separated by a single comma")

def generate_summary():
    """Calculates and shows summary statistics (In one command not individually)"""
    if not grades:
        summary_label.config(text="No data entered.") # Acts as an error catch, if the users input is not numbers (not float) or if theres nothing entered at all
        return
# Sets the summary information (In version 1 this is all as one function)
    highest = max(grades)
    lowest = min(grades)
    average = sum(grades) / len(grades)
    sorted_grades = sorted(grades)
    
    # median calculation
    n = len(sorted_grades)
    if n % 2 == 1:
        median = sorted_grades[n // 2] # This finds the median if there is an odd number of grades.
    else:
        median = (sorted_grades[n//2 - 1] + sorted_grades[n//2]) / 2 # This finds the median (if there is an even number of grades, this finds the average of the two middle numbers).

    summary_text = (
        f"Highest: {highest}\n"
        f"Lowest: {lowest}\n"
        f"Average: {average:.2f}\n"
        f"Median: {median}"
    )

    summary_label.config(text=summary_text)

# ---------------- Frames -------------------
ask_frame = tk.Frame(root) # Asks the user if they want to use the program
input_frame = tk.Frame(root) # This is where the user can input their data (grades, names etc.)
ask_sum_frame = tk.Frame(root) # This is the question frame for the summary
sum_frame = tk.Frame(root) # This is the frame for the summary itself
exit_frame = tk.Frame(root) # This is the exit frame, thanking the user for using the program

# Using a loop to bring forward the frames
for frame in (ask_frame, input_frame, ask_sum_frame, sum_frame, exit_frame):
    frame.place(relwidth=1, relheight=1) # Sets frames relative height and width

# ---------------- Posing Question -------------------
img1 = Image.open("welcome.png") # Gives the user a nice welcoming message
img1 = img1.resize((600, 400)) # Re-sizes the image to be 600 x 400 pixels
photo1 = ImageTk.PhotoImage(img1)

tk.Label(ask_frame, text="Would You Like To Input Data?").pack()
tk.Label(ask_frame, image=photo1).pack()

tk.Button(ask_frame, text="Yes", # Creates A button that brings the user to the data frame 
          command=lambda: show_frame(input_frame)).pack()

tk.Button(ask_frame, text="No",
          command=lambda: show_frame(exit_frame)).pack()

# ----------------- Inputting Data --------------------
tk.Label(input_frame, text="Please Enter Your Data (comma separated)").pack()

entry = tk.Entry(input_frame)
entry.pack()

result_label = tk.Label(input_frame, text="")
result_label.pack()

tk.Button(input_frame, text="Enter",
          command=process_input).pack()

tk.Button(input_frame, text="Back",
          command=lambda: show_frame(ask_frame)).pack()

# ----------------- Key for Summary ------------------
tk.Label(input_frame, text="Grading Key:\n<25 = Not Achieved\n25-49 = Achieved\n50-74 = Merit\n75-100 = Excellence").pack(side="bottom")

# ----------------- Ask Summary Frame ------------------
tk.Label(ask_sum_frame, text="Would you like a summary?").pack()

tk.Button(ask_sum_frame, text="Yes",
          command=lambda: [generate_summary(), show_frame(sum_frame)]).pack()

tk.Button(ask_sum_frame, text="No",
          command=lambda: show_frame(exit_frame)).pack()

# ----------------- Summary Frame ----------------------
tk.Label(sum_frame, text="Summary").pack()

summary_label = tk.Label(sum_frame, text="")
summary_label.pack()

tk.Button(sum_frame, text="Back to Start",
          command=lambda: show_frame(ask_frame)).pack()

# --------------------- Exit Frame ----------------------
img2 = Image.open("exit.png") # Gives the user A thank you message, after using this program
img2 = img2.resize((600, 400))
photo2 = ImageTk.PhotoImage(img2)

tk.Label(exit_frame, text="Thanks for using the program!").pack()
tk.Label(exit_frame, image=photo2).pack()

tk.Button(exit_frame, text="Exit",
          command=root.destroy).pack() # .destroy closes the program immediately, like an exit function.

ask_frame.image = photo1
exit_frame.image = photo2

show_frame(ask_frame) # Shows the first frame to the user
root.mainloop()