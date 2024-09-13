import pyvisa
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
"""
This code allows to create a GUI in order to communicate with DG535 Pulse Shaper/Delay Generator.
It works mainly according to MuEDM 09/2024 beam test requirements.

You can set delays for each channel and also choose the reference.

You can modify trigger settings (every setting is selectable but not every function is developed for not required ones).
The main focus is on INT trigger, of which you can select the RATE.
You can also switch to Single Shot mode (for instance, to stop the trigger).

For every trigger mode you can select the slope (Raising or Falling).
"""

class MainWindow(QMainWindow): #RIcorda di riaggiungere l'eredità
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("DG535 Working Interface")
        self.setGeometry(500, 100, 400, 500)

        # Connect to the DG535 device
        self.connect_to_dg535()

        # Set up the UI
        self.setup_ui()

        # Initialize dummy variables
        self.refresh_settings()


    def connect_to_dg535(self):
        """Initialize the VISA resource manager and connect to DG535."""
        self.rm = pyvisa.ResourceManager()
        devices = self.rm.list_resources()
        print(f"Available devices: {devices}")

        # Assuming the DG535 is the only GPIB device connected
        dg535_address = [device for device in devices if "GPIB" in device][0]
        self.dg535 = self.rm.open_resource(dg535_address)

    def setup_ui(self):

        # Set up the main layout
        general_layout = QVBoxLayout()

        # Connection Layout
        connection_layout = QVBoxLayout()
        connection_label = QLabel(f"...Connected to DG535...")
        connection_layout.addWidget(connection_label)

        # Settings Layout
        settings_layout = QVBoxLayout()
        settings_label = QLabel("• Current settings:")
        trigger_label_1 = QLabel(f"     - Trigger mode: {self.trigger_mode}.")
        trigger_label_2 = QLabel(f"     - Trigger slope: {self.trigger_slope}.")
        trigger_label_3 = QLabel(f"     - Trigger rate: {self.trigger_rate} Hz.")
        settings_layout.addWidget(settings_label)
        settings_layout.addWidget(trigger_label_1)
        settings_layout.addWidget(trigger_label_2)
        settings_layout.addWidget(trigger_label_3)

        # Delays Layout
        delays_layout = QVBoxLayout()
        delays_label = QLabel("• Delays:")
        delays_label_1 = QLabel(f"      - T0: {self.delay_T0} s")
        delays_label_2 = QLabel(f"      - A: {self.delay_A} s")
        delays_label_3 = QLabel(f"      - B: {self.delay_B} s")
        delays_label_4 = QLabel(f"      - AB: {self.delay_AB} s")
        delays_label_5 = QLabel(f"      - C: {self.delay_C} s")
        delays_label_6 = QLabel(f"      - D: {self.delay_D} s")
        delays_label_7 = QLabel(f"      - CD: {self.delay_CD} s")
        delays_layout.addWidget(delays_label)
        delays_layout.addWidget(delays_label_1)
        delays_layout.addWidget(delays_label_2)
        delays_layout.addWidget(delays_label_3)
        delays_layout.addWidget(delays_label_4)
        delays_layout.addWidget(delays_label_5)
        delays_layout.addWidget(delays_label_6)
        delays_layout.addWidget(delays_label_7)

        # Buttons Layout
        pressable_layout = QHBoxLayout()
        refresh_button = QPushButton("Refresh")
        modify_button = QPushButton("Modify")
        store_button = QPushButton("Store")
        recall_button = QPushButton("Recall")

        # Connect button signals to their slots
        refresh_button.clicked.connect(self.refresh_settings)
        modify_button.clicked.connect(self.open_modify_window)
        store_button.clicked.connect(self.store_settings)
        recall_button.clicked.connect(self.recall_settings)

        pressable_layout.addWidget(refresh_button)
        pressable_layout.addWidget(modify_button)
        pressable_layout.addWidget(store_button)
        pressable_layout.addWidget(recall_button)

        # General Layout Assembly
        general_layout.addLayout(connection_layout)
        general_layout.addLayout(settings_layout)
        general_layout.addLayout(delays_layout)
        general_layout.addLayout(pressable_layout)

        # Set the layout for the central widget
        central_widget = QWidget()
        central_widget.setLayout(general_layout)
        self.setCentralWidget(central_widget)


    def open_modify_window(self):
        # Create an instance of the secondary window and show it
        self.modify_window = SecondaryWindow()
        self.modify_window.show()

    def refresh_settings(self):
        """Refresh the settings from the DG535 and update UI elements."""
        # Query the DG535 for the latest settings
        self.trigger_rate = self.dg535.query("TR?").strip()
        self.trigger_mode = self.dg535.query("TM?").strip()
        self.trigger_slope = self.dg535.query("TS?").strip()
        self.delay_T0 = self.dg535.query("DT? 1").strip()
        self.delay_A = self.dg535.query("DT? 2").strip()
        self.delay_B = self.dg535.query("DT? 3").strip()
        self.delay_AB = self.dg535.query("DT? 4").strip()
        self.delay_C = self.dg535.query("DT? 5").strip()
        self.delay_D = self.dg535.query("DT? 6").strip()
        self.delay_CD = self.dg535.query("DT? 7").strip()

        # Update the UI elements
        self.trigger_label_1.setText(f"     - Trigger mode: {self.trigger_mode}.")
        self.trigger_label_2.setText(f"     - Trigger slope: {self.trigger_slope}.")
        self.trigger_label_3.setText(f"     - Trigger rate: {self.trigger_rate} Hz.")
        self.delays_label_1.setText(f"      - T0: {self.delay_T0} s")
        self.delays_label_2.setText(f"      - A: {self.delay_A} s")
        self.delays_label_3.setText(f"      - B: {self.delay_B} s")
        self.delays_label_4.setText(f"      - AB: {self.delay_AB} s")
        self.delays_label_5.setText(f"      - C: {self.delay_C} s")
        self.delays_label_6.setText(f"      - D: {self.delay_D} s")
        self.delays_label_7.setText(f"      - CD: {self.delay_CD} s")

    def store_settings(self):
        """Store the current settings in a slot (1-9)."""
        # Ask user to select a slot for storing settings
        slot, ok = QInputDialog.getInt(self, "Store Settings", "Select a slot (1-9):", min=1, max=9, step=1)

        if ok:
            try:
                # Send store command to DG535
                self.dg535.write(f"ST {slot}")
                QMessageBox.information(self, "Success", f"Settings stored in slot {slot}.")
            except pyvisa.VisaIOError as e:
                QMessageBox.critical(self, "Error", f"Failed to store settings: {e}")

    def recall_settings(self):
        """Recall settings from a selected slot (1-9)."""
        # Ask user to select a slot for recalling settings
        slot, ok = QInputDialog.getInt(self, "Recall Settings", "Select a slot (1-9):", min=1, max=9, step=1)

        if ok:
            try:
                # Send recall command to DG535
                self.dg535.write(f"RC {slot}")
                QMessageBox.information(self, "Success", f"Settings recalled from slot {slot}.")
                self.refresh_settings()  # Refresh settings to update the UI
            except pyvisa.VisaIOError as e:
                QMessageBox.critical(self, "Error", f"Failed to recall settings: {e}")



class SecondaryWindow(QWidget): #RIcorda di riaggiungere l'eredità
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modify the settings")
        self.resize(600,100)
        self.setup_ui()

    def setup_ui(self):
        # Set up the layout for the secondary window
        modify_window_layout = QVBoxLayout()

        # trigger_mode_layout
        trigger_mode_layout = QHBoxLayout()
        # Add a QLineEdit (text box) to the layout
        trigger_mode_label = QLabel("- TRIGGER MODE (INT=0, EXT=1, SS=2, BURST=3)")
        trigger_mode_line = QLineEdit()
        trigger_mode_line.setPlaceholderText("Enter trigger mode...")
        # Add the button
        trigger_mode_button = QPushButton("Enter")
        trigger_mode_button.clicked.connect(self.write_on_dg535_tm)

        # Add widget to the layout
        trigger_mode_layout.addWidget(trigger_mode_label)
        trigger_mode_layout.addWidget(trigger_mode_line)
        trigger_mode_layout.addWidget(trigger_mode_button)

        # trigger_rate_layout
        trigger_rate_layout = QHBoxLayout()
        # Add a QLineEdit (text box) to the layout
        trigger_rate_label = QLabel("- TRIGGER RATE [Hz]")
        trigger_rate_line = QLineEdit()
        trigger_rate_line.setPlaceholderText("Enter trigger rate...")
        # Add the button
        trigger_rate_button = QPushButton("Enter")
        trigger_rate_button.clicked.connect(self.write_on_dg535_tr)

        # Add widget to the layout
        trigger_rate_layout.addWidget(trigger_rate_label)
        trigger_rate_layout.addWidget(trigger_rate_line)
        trigger_rate_layout.addWidget(trigger_rate_button)

        # trigger_slope_layout
        trigger_slope_layout = QHBoxLayout()
        # Add a QLineEdit (text box) to the layout
        trigger_slope_label = QLabel("- TRIGGER SLOPE (FALLING=0, RAISING=1)")
        trigger_slope_line = QLineEdit()
        trigger_slope_line.setPlaceholderText("Enter trigger slope...")
        # Add the button
        trigger_slope_button = QPushButton("Enter")
        trigger_slope_button.clicked.connect(self.write_on_dg535_ts)

        # Add widget to the layout
        trigger_slope_layout.addWidget(trigger_slope_label)
        trigger_slope_layout.addWidget(trigger_slope_line)
        trigger_slope_layout.addWidget(trigger_slope_button)

        # Define all the layout for delays
        delay_t0_layout = QHBoxLayout()
        delay_a_layout = QHBoxLayout()
        delay_b_layout = QHBoxLayout()
        delay_ab_layout = QHBoxLayout()
        delay_c_layout = QHBoxLayout()
        delay_d_layout = QHBoxLayout()
        delay_cd_layout = QHBoxLayout()

        # Create label to be shown in the central widget
        delay_info_label0 = QLabel("")
        delay_info_label1 = QLabel("To change delay use this notation: i,j")
        delay_info_label2 = QLabel("i = channel to refer for the delay, j = seconds of delay")

        # Labels for channels
        delay_t0_label = QLabel("Channel T0")
        delay_a_label = QLabel("Channel A")
        delay_b_label = QLabel("Channel B")
        delay_ab_label = QLabel("Channel AB")
        delay_c_label = QLabel("Channel C")
        delay_d_label = QLabel("Channel D")
        delay_cd_label = QLabel("Channel CD")

        delay_t0_line = QLineEdit()
        delay_a_line = QLineEdit()
        delay_b_line = QLineEdit()
        delay_ab_line = QLineEdit()
        delay_c_line = QLineEdit()
        delay_d_line = QLineEdit()
        delay_cd_line = QLineEdit()

        delay_t0_line.setPlaceholderText("Enter command here...")
        delay_a_line.setPlaceholderText("Enter command here...")
        delay_b_line.setPlaceholderText("Enter command here...")
        delay_ab_line.setPlaceholderText("Enter command here...")
        delay_c_line.setPlaceholderText("Enter command here...")
        delay_d_line.setPlaceholderText("Enter command here...")
        delay_cd_line.setPlaceholderText("Enter command here...")

        delay_t0_button = QPushButton("press")
        delay_a_button = QPushButton("press")
        delay_b_button = QPushButton("press")
        delay_ab_button = QPushButton("press")
        delay_c_button = QPushButton("press")
        delay_d_button = QPushButton("press")
        delay_cd_button = QPushButton("press")

        delay_t0_button.clicked.connect(self.write_on_dg535_dtt0)
        delay_a_button.clicked.connect(self.write_on_dg535_dta)
        delay_b_button.clicked.connect(self.write_on_dg535_dtb)
        delay_ab_button.clicked.connect(self.write_on_dg535_dtab)
        delay_c_button.clicked.connect(self.write_on_dg535_dtc)
        delay_d_button.clicked.connect(self.write_on_dg535_dtd)
        delay_cd_button.clicked.connect(self.write_on_dg535_dtcd)

        delay_t0_layout.addWidget(delay_t0_label)
        delay_t0_layout.addWidget(delay_t0_line)
        delay_t0_layout.addWidget(delay_t0_button)

        delay_a_layout.addWidget(delay_a_label)
        delay_a_layout.addWidget(delay_a_line)
        delay_a_layout.addWidget(delay_a_button)

        delay_b_layout.addWidget(delay_b_label)
        delay_b_layout.addWidget(delay_b_line)
        delay_b_layout.addWidget(delay_b_button)

        delay_ab_layout.addWidget(delay_ab_label)
        delay_ab_layout.addWidget(delay_ab_line)
        delay_ab_layout.addWidget(delay_ab_button)

        delay_c_layout.addWidget(delay_c_label)
        delay_c_layout.addWidget(delay_c_line)
        delay_c_layout.addWidget(delay_c_button)

        delay_d_layout.addWidget(delay_d_label)
        delay_d_layout.addWidget(delay_d_line)
        delay_d_layout.addWidget(delay_d_button)

        delay_cd_layout.addWidget(delay_cd_label)
        delay_cd_layout.addWidget(delay_cd_line)
        delay_cd_layout.addWidget(delay_cd_button)

        trigger_layout = QVBoxLayout()

        trigger_layout.addLayout(trigger_mode_layout)
        trigger_layout.addLayout(trigger_rate_layout)
        trigger_layout.addLayout(trigger_slope_layout)

        delay_layout = QVBoxLayout()

        delay_layout.addWidget(delay_info_label)
        delay_layout.addWidget(delay_info_label2)

        delay_layout.addLayout(delay_t0_layout)
        delay_layout.addLayout(delay_a_layout)
        delay_layout.addLayout(delay_b_layout)
        delay_layout.addLayout(delay_ab_layout)
        delay_layout.addLayout(delay_c_layout)
        delay_layout.addLayout(delay_d_layout)
        delay_layout.addLayout(delay_cd_layout)

        modify_window_layout.addLayout(trigger_layout)
        modify_window_layout.addLayout(delay_layout)

        self.setLayout(modify_window_layout)

    def write_on_dg535_tm(self):
        # Write the code in the machine and execute it
        self.dg535.write(f"TM {trigger_mode_line}")
        if trigger_mode_line == 2:
            self.dg535.write(f"SS") # Need this to trigger once after changing trigger mode

    def write_on_dg535_tr(self):
        # Write the code in the machine and execute it
        self.dg535.write(f"TR {trigger_rate_line}")

    def write_on_dg535_ts(self):
        # Write the code in the machine and execute it
        self.dg535.write(f"TS {trigger_slope_line}")

    def write_on_dg535_dtt0(self):
        # Write the code in the machine and execute it
        self.dg535.write(f"DT 1,{delay_t0_line}")

    def write_on_dg535_dta(self):
        # Write the code in the machine and execute it
        self.dg535.write(f"DT 2,{delay_a_line}")

    def write_on_dg535_dtb(self):
        # Write the code in the machine and execute it
        self.dg535.write(f"DT 3,{delay_b_line}")

    def write_on_dg535_dtab(self):
        # Write the code in the machine and execute it
        self.dg535.write(f"DT 4,{delay_ab_line}")

    def write_on_dg535_dtc(self):
        # Write the code in the machine and execute it
        self.dg535.write(f"DT 5,{delay_c_line}")

    def write_on_dg535_dtd(self):
        # Write the code in the machine and execute it
        self.dg535.write(f"DT 6,{delay_d_line}")

    def write_on_dg535_dtcd(self):
        # Write the code in the machine and execute it
        self.dg535.write(f"DT 7,{delay_cd_line}")


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
