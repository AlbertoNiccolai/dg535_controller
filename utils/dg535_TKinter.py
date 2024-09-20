import tkinter as tk
from tkinter import ttk
import pyvisa

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.title("DG535 Working Interface")
        self.geometry("400x500")

        # Connect to the DG535 device
        self.connect_to_dg535()

        # Set up the UI
        self.setup_ui()

    def connect_to_dg535(self):
        """Initialize the VISA resource manager and connect to DG535."""
        self.rm = pyvisa.ResourceManager()
        devices = self.rm.list_resources()
        print(f"Available devices: {devices}")

        # Assuming the DG535 is the only GPIB device connected
        self.dg535_address = [device for device in devices if "GPIB" in device][0]
        self.dg535 = self.rm.open_resource(self.dg535_address)

    def setup_ui(self):
        # Main layout setup
        general_frame = ttk.Frame(self)
        general_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Connection info
        connection_label = ttk.Label(general_frame, text=f"...Connected to {self.dg535_address}...")
        connection_label.pack(pady=5)

        # Create frames for settings input
        settings_frame = ttk.Frame(general_frame)
        settings_frame.pack(pady=10)

        # Delay inputs (T0, A, B, C, D)
        self.create_delay_input(settings_frame, "T0")
        self.create_delay_input(settings_frame, "A")
        self.create_delay_input(settings_frame, "B")
        self.create_delay_input(settings_frame, "C")
        self.create_delay_input(settings_frame, "D")

        # Trigger rate and slope inputs
        self.trigger_rate_entry = self.create_labeled_entry(settings_frame, "Trigger Rate")
        self.trigger_slope_entry = self.create_labeled_entry(settings_frame, "Trigger Slope")

        # Buttons for triggering actions
        trigger_button_frame = ttk.Frame(general_frame)
        trigger_button_frame.pack(pady=10)

        set_trigger_button = ttk.Button(trigger_button_frame, text="Set Trigger Mode", command=self.write_on_dg535_tm)
        set_trigger_button.pack(side=tk.LEFT, padx=5)

        set_rate_button = ttk.Button(trigger_button_frame, text="Set Trigger Rate", command=self.write_on_dg535_tr)
        set_rate_button.pack(side=tk.LEFT, padx=5)

        set_slope_button = ttk.Button(trigger_button_frame, text="Set Trigger Slope", command=self.write_on_dg535_ts)
        set_slope_button.pack(side=tk.LEFT, padx=5)

    def create_delay_input(self, parent, delay_name):
        """Helper function to create delay input fields."""
        delay_frame = ttk.Frame(parent)
        delay_frame.pack(pady=5, fill='x')

        delay_label = ttk.Label(delay_frame, text=f"Delay {delay_name}:")
        delay_label.pack(side=tk.LEFT)

        delay_entry = ttk.Entry(delay_frame)
        delay_entry.pack(side=tk.LEFT, padx=5)

        # Save the entry to access later when writing commands to the device
        setattr(self, f"delay_{delay_name.lower()}_entry", delay_entry)

    def create_labeled_entry(self, parent, label_text):
        """Helper function to create labeled entry fields."""
        frame = ttk.Frame(parent)
        frame.pack(pady=5, fill='x')

        label = ttk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT)

        entry = ttk.Entry(frame)
        entry.pack(side=tk.LEFT, padx=5)

        return entry

    # Methods to write to the DG535 device based on user input
    def write_on_dg535_tm(self):
        trigger_mode_line = self.trigger_rate_entry.get()  # Get trigger mode input
        self.dg535.write(f"TM {trigger_mode_line}")
        if trigger_mode_line == '2':  # Single shot mode
            self.dg535.write(f"SS")  # Trigger once after changing trigger mode

    def write_on_dg535_tr(self):
        trigger_rate_line = self.trigger_rate_entry.get()  # Get trigger rate input
        self.dg535.write(f"TR {trigger_rate_line}")

    def write_on_dg535_ts(self):
        trigger_slope_line = self.trigger_slope_entry.get()  # Get trigger slope input
        self.dg535.write(f"TS {trigger_slope_line}")

    def write_on_dg535_delay(self, delay_type):
        delay_value = getattr(self, f"delay_{delay_type}_entry").get()  # Get delay input
        delay_map = {"t0": 1, "a": 2, "b": 3, "c": 5, "d": 6}
        self.dg535.write(f"DT {delay_map[delay_type]},{delay_value}")

# Main function equivalent to the QApplication loop in PyQt6
def main():
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
