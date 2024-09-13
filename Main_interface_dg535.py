import tkinter as tk
import subprocess

# Function to run a.py
def run_script_a():
    subprocess.run(["python", "utils/Interfacedg535.py"])

# Function to run b.py
def run_script_b():
    subprocess.run(["python", "utils/prova_dg535_interfaccia.py"])

# Create the main window
window = tk.Tk()
window.title("Script Runner")

# Set window size
window.geometry("300x150")

# Create Button for running a.py
button_a = tk.Button(window, text="Run Script A", command=run_script_a)
button_a.pack(pady=20)

# Create Button for running b.py
button_b = tk.Button(window, text="Run Script B", command=run_script_b)
button_b.pack(pady=20)

# Start the Tkinter event loop
window.mainloop()

