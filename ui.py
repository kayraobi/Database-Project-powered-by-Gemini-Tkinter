import tkinter
import customtkinter
import sqlite3
from AppointmentStore import *
from AppointmentWindow import *
from SetAppointmentWindow import *

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect("hospital3.db")
        self.appointment_store = AppointmentStore(self.conn)

        # configure window
        self.title("Hospital Appointment System")
        self.geometry("1100x580")

        # Buttons
        self.set_appointment_btn = customtkinter.CTkButton(
            self, text="Set an Appointment", command=self.set_appointment)
        self.set_appointment_btn.grid(row=1, column=0, padx=20, pady=10)

        self.get_appointments_btn = customtkinter.CTkButton(
            self, text="Appointments", command=self.get_appointments)
        self.get_appointments_btn.grid(row=2, column=0, padx=20, pady=10)

    def set_appointment(self):
        print("Opening SetAppointmentWindow")
        set_appointment_window = SetAppointmentWindow(self.conn)
        set_appointment_window.show()

    def get_appointments(self):
        print("Opening AppointmentWindow")
        appointment_window = AppointmentWindow(self.conn)
        appointment_window.show()

if __name__ == "__main__":
    customtkinter.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"
    app = App()
    app.mainloop()