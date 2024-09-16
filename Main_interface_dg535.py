import tkinter as tk
import subprocess
from tkinter import messagebox

def run_script_a():
    subprocess.run(["python", "utils/Interfacedg535.py"])


def run_script_b():
    subprocess.run(["python", "utils/prova_dg535_interfaccia.py"])




def show_help():
    """
    Function to display the help window.
    """
    help_message = (
        "Pulse Generator Interface Help\n\n"

        "Choose the first interface for a simpler workflow\n"
        "Choose the fine tune interface in case a more detailed control of the pulse generator is needed\n"
    )
    messagebox.showinfo("Help", help_message)





# Create the main window
window = tk.Tk()
window.title("Interface hub")


# Create a menu bar
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# Create a Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Help", command=show_help)


#set size
window.geometry("600x300")

#button to run simple interface
button_a = tk.Button(window, text="Run simplified interface", command=run_script_a)
button_a.pack(pady=20)

#button to run fine-tune interface
button_b = tk.Button(window, text="Run fine-tuning interface", command=run_script_b)
button_b.pack(pady=20)

# Start the Tkinter event loop
window.mainloop()

