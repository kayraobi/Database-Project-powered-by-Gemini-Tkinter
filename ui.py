import tkinter as tk
import customtkinter
import sqlite3
from AppointmentStore import *
from AppointmentWindow import *
from SetAppointmentWindow import *
from PatientCreateWindow import *

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect("hospital3.db")
        self.appointment_store = AppointmentStore(self.conn)

        self.set_window_open = False  # Track if SetAppointmentWindow is open
        self.appointment_window_open = False  # Track if AppointmentWindow is open

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
        
        #self.set_patient_btn = customtkinter.CTkButton(self, text = "Create id", command = self.set_patient)
        #self.set_patient_btn.grid(row=2, column=0, padx=20, pady=10)

    def set_appointment(self):
        if self.set_window_open:
            return  # Do nothing if window is already open
        print("Opening SetAppointmentWindow")
        self.set_window_open = True
        self.set_appointment_window = SetAppointmentWindow(self.conn)
        self.set_appointment_window.protocol("WM_DELETE_WINDOW", self.close_set_window)
        self.set_appointment_window.show()

    def close_set_window(self):
        self.set_window_open = False
        self.set_appointment_window.destroy()

    def get_appointments(self):
        if self.appointment_window_open:
            return
        print("Opening AppointmentWindow")
        self.appointment_window_open = True
        self.appointment_window = AppointmentWindow(self.conn)
        self.appointment_window.protocol("WM_DELETE_WINDOW", self.close_appointment_window)
        self.appointment_window.show()

    def close_appointment_window(self):
        self.appointment_window_open = False
        self.appointment_window.destroy()
        
    #def set_patient(self):
    # self.patient_create_window = PatientCreateWindow(self.conn)
     #self.appointment_window.show() 
        
        
        
        
        

if __name__ == "__main__":
    customtkinter.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"
    app = App()
    app.mainloop()